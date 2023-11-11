from dataclasses import dataclass
from donnes_pipe.connector_interfaces import ConnectorELT, ConnectClient
from .transformations import get_cat_api_transformers


@dataclass
class CatsConnector(ConnectorELT):
    def extract_data(self, source_client: ConnectClient) -> dict:
        results = {}

        with source_client.connect() as client:
            results.update({
                "breeds": client.api.get_breeds(),
            }) 

            return results

    # Code to transform the data
    def transform_data(self, raw_data):
        current_transformation = get_cat_api_transformers('basic_info')

        basic_breeds_info = current_transformation.get_info(raw_data.get('breeds'))
        social_and_inteligent_cats = current_transformation.mark_social_and_inteligent_cats(basic_breeds_info)
    
        results = {
            "breeds": social_and_inteligent_cats
        }

        return results

    # Code to load the data into the destination database
    def load_data(self, data, destination_client: ConnectClient):
        with destination_client.connect() as client:
            print(client["create"])

    # orchestrates the extract, transform, load process
    def run(
        self,
        source_client: ConnectClient,
        destination_client: ConnectClient,
    ):
        data = self.extract_data(source_client=source_client)
        self.transform_data(data)
        self.load_data(data, destination_client=destination_client)
