# Code to extract data from the source database
import json
from typing import Any
import os
from dotenv import load_dotenv
import requests
from dataclasses import dataclass, field
from connector_interfaces import ConnectorELT, ConnectClient, ConnectorTransformer
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


def make_request(method: str, url: str, **kwargs) -> Any:
    response = None
    try:
        response = requests.request(method, url, **kwargs)
        return response.json()
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {str(e)} || Server response: {response.text}")
        return response
    except Exception as e:
        print(f"Error on request: {str(e)}")
        return response


@dataclass
class CatAPIClient(ConnectClient):
    name: str = "Cat API Client"
    type: str = "api"
    API_URL = "https://api.thecatapi.com/v1"
    api: "CatAPIClient.Api" = None

    def __post_init__(self):
        self.headers = {"x-api-key": self.config["api_key"]}

    @contextmanager
    def connect(self):
        try:
            response = requests.get(self.API_URL + "/breeds/2", headers=self.headers)

            if response.status_code != 200:
                raise Exception(f"Connection failed to {self.name}")

            self.api = self.Api(url=self.API_URL, headers=self.headers)
            yield self
        except Exception as e:
            raise e

    @dataclass
    class Api:
        url: str
        headers: dict = field(default_factory=dict)

        def get_breeds(self):
            return make_request(
                method="GET", url=self.url + "/breeds", headers=self.headers
            )

        def get_images(self):
            return make_request(
                method="GET", url=self.url + "/images/search", headers=self.headers
            )

        def get_favourites(self):
            return make_request(
                method="GET", url=self.url + "/favourites", headers=self.headers
            )


@dataclass
class PostgreSqlClient(ConnectClient):
    name: str = "PostgreSql Client"
    type: str = "db"
    DB_URL = "https://localhost:5432"

    @contextmanager
    def connect(self):
        try:
            ## here is the code to connect to the database if connection is successful, return db client
            yield {
                "create": "saving data",
                "delete": "deleting data",
                "edit": "editing data",
            }
        except Exception as e:
            raise e


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
