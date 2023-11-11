from dataclasses import dataclass, field
from donnes_stream.connector_interfaces import ConnectorELT, ConnectClient, ConnectorTransformer
from contextlib import contextmanager
import requests


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

