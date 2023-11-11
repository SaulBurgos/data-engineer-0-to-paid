"""
This module contains a factory function to create connector clients.
"""

from .connector_interfaces import ConnectClient
from .clients.cat_client import CatAPIClient
from .clients.postgre_client import PostgreSqlClient

CONNECTORS_CLIENTS: dict[str, ConnectClient] = {}
CONNECTORS_CLIENTS["cat_api_client"] = lambda config={}: CatAPIClient(config=config)
CONNECTORS_CLIENTS["postgre_client"] = lambda config={}: PostgreSqlClient(config=config)


def get_connector_client(name: str) -> ConnectClient:
    """
    Returns a connector client based on the given name.

    Args:
        name (str): The name of the connector client.

    Returns:
        ConnectClient: The connector client instance.

    Raises:
        ValueError: If the connector client with the given name is not found.
    """
    if name not in CONNECTORS_CLIENTS:
        raise ValueError(f"Connector {name} not found")
    return CONNECTORS_CLIENTS[name]
