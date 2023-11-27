import os
from dotenv import load_dotenv
from donnes_pipe.client_factory import get_connector_client
from connectors.cat_connector import CatsConnector
from connectors.public_api_connector import PublicApisConnector

load_dotenv()

if __name__ == "__main__":
    # CAT API CONNECTOR
    # source_client = get_connector_client("cat_api_client")(
    #     config={"api_key": os.environ["CAT_API_KEY"]}
    # )
    # destination_client = get_connector_client("postgre_client")(
    #     config={"host": "localhost", "port": 5432}
    # )
    # CatsConnector().run(
    #     source_client=source_client,
    #     destination_client=destination_client,
    # )

    # PUBLIC API CONNECTOR
    source_client = get_connector_client("public_api_client")(config={})
    destination_client = get_connector_client("file_client")(config={})

    PublicApisConnector().run(
        source_client=source_client,
        destination_client=destination_client,
    )

    
    