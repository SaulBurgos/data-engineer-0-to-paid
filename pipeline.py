import os
from dotenv import load_dotenv
from donnes_pipe.client_factory import get_connector_client
from connectors.cat_connector import CatsConnector

load_dotenv()

if __name__ == "__main__":
    source_client = get_connector_client("cat_api_client")(
        config={"api_key": os.environ["CAT_API_KEY"]}
    )
    destination_client = get_connector_client("postgre_client")(
        config={"host": "localhost", "port": 5432}
    )
    CatsConnector().run(
        source_client=source_client,
        destination_client=destination_client,
        transformations=["type3", "type2", "type1"],
    )
