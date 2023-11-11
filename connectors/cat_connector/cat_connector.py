from dataclasses import dataclass
from donnes_pipe.connector_interfaces import ConnectorELT, ConnectClient
from .transformations import get_cat_api_transformers


@dataclass
class CatsConnector(ConnectorELT):
    def extract_data(self, source_client: ConnectClient):
        with source_client.connect() as client:
            print(client.api.get_breeds())

    # Code to transform the data
    def transform_data(self, raw_data, transformations: list[str]):
        transformed_data = raw_data

        for transformer in transformations:
            current_transformation = get_cat_api_transformers(transformer)
            transformed_data = current_transformation.apply(transformed_data)

        return transformed_data

    # Code to load the data into the destination database
    def load_data(self, data, destination_client: ConnectClient):
        with destination_client.connect() as client:
            print(client["create"])

    # orchestrates the extract, transform, load process
    def run(
        self,
        source_client: ConnectClient,
        destination_client: ConnectClient,
        transformations: list[str],
    ):
        data = self.extract_data(source_client=source_client)
        self.transform_data(data, transformations=transformations)
        self.load_data(data, destination_client=destination_client)
