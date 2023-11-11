import os
from dotenv import load_dotenv
from donnes_pipe.clients.cat_client import CatAPIClient
from donnes_pipe.clients.postgre_client import PostgreSqlClient
from connectors.cat_connector import CatsConnector

load_dotenv()

if __name__ == "__main__":
    source_client = CatAPIClient(config={"api_key": os.environ["CAT_API_KEY"]})
    destination_client = PostgreSqlClient(config={"host": "localhost", "port": 5432})
    CatsConnector().run(
        source_client=source_client,
        destination_client=destination_client,
        transformations=["type3", "type2", "type1"],
    )
