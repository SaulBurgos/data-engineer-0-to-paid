from dataclasses import dataclass
from donnes_pipe.connector_interfaces import ConnectorELT, ConnectClient
from donnes_pipe.clients.public_api_client import PublicAPIsClient
from donnes_pipe.clients.file_client import FileClient
from .transformations import PublicBasicInfoTransformation


@dataclass
class PublicApisConnector(ConnectorELT):
    def extract_data(self, source_client: ConnectClient) -> dict:
        results = {}

        with source_client.connect() as _client:
            client: PublicAPIsClient = _client
            results = client.api.get_entries()
            return results

    # Code to transform the data
    def transform_data(self, raw_data):
        result = PublicBasicInfoTransformation().get_basic_info(
            raw_data=raw_data.get("entries")
        )
        return result

    # Code to load the data into the destination database
    def load_data(self, data, destination_client: ConnectClient):
        with destination_client.connect() as _client:
            client: FileClient = _client
            client.write_file(data=data, filename="public_apis_list", extension="json")

    # orchestrates the extract, transform, load process
    def run(
        self,
        source_client: ConnectClient,
        destination_client: ConnectClient,
    ):
        data = self.extract_data(source_client=source_client)
        transform_data = self.transform_data(data)
        self.load_data(transform_data, destination_client=destination_client)
