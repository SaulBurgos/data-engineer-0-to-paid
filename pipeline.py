# Code to extract data from the source database
import json
from typing import Any
import os
from dotenv import load_dotenv
import requests
from dataclasses import dataclass, field
from donnes_stream.connector_interfaces import ConnectorELT, ConnectClient, ConnectorTransformer
from donnes_stream.clients.cat_client import CatAPIClient
from donnes_stream.clients.postgre_client import PostgreSqlClient
from contextlib import contextmanager

load_dotenv()


@dataclass
class CatTranformType1(ConnectorTransformer):
    description: str = "This will create a unique object with all breeds in one place"
    verison: str = "1.0"

    def apply(self, data):
        return data


@dataclass
class CatTranformType2(ConnectorTransformer):
    description: str = "This will create a unique object with all breeds in one place"
    verison: str = "1.0"

    def apply(self, data):
        return data


@dataclass
class CatTranformType3(ConnectorTransformer):
    description: str = (
        "this will join all the breeds in one place with a date of last year"
    )
    verison: str = "1.0"

    def apply(self, data):
        return data


def get_catConnector_transformer(transformer_name) -> ConnectorTransformer:
    factory = {
        "deafult": CatTranformType1,
        "type1": CatTranformType1,
        "type2": CatTranformType2,
        "type3": CatTranformType3,
    }

    if transformer_name not in factory:
        raise Exception(f"Unknown transformer: {transformer_name}")

    return factory[transformer_name]()

@dataclass
class CatsConnector(ConnectorELT):
    def extract_data(self, source_client: ConnectClient):
        with source_client.connect() as client:
            print(client.api.get_breeds())

    # Code to transform the data
    def transform_data(self, raw_data, transformations: list[str]):
        transformed_data = raw_data

        for transformer in transformations:
            current_transformation = get_catConnector_transformer(transformer)
            transformed_data = current_transformation.apply(transformed_data)

        return transformed_data

    # Code to load the data into the destination database
    def load_data(self, data, destination_client: ConnectClient):
        with destination_client.connect() as client:
            print(client["create"])

    def run(
        self,
        source_client: ConnectClient,
        destination_client: ConnectClient,
        transformations: list[str],
    ):
        data = self.extract_data(source_client=source_client)
        self.transform_data(data, transformations=transformations)
        self.load_data(data, destination_client=destination_client)


if __name__ == "__main__":
    source_client = CatAPIClient(config={"api_key": os.environ["CAT_API_KEY"]})
    destination_client = PostgreSqlClient(config={"host": "localhost", "port": 5432})
    CatsConnector().run(
        source_client=source_client,
        destination_client=destination_client,
        transformations=["type3", "type2", "type1"],
    )
