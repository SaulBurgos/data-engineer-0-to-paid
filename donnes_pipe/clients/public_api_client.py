import requests
from contextlib import contextmanager
from dataclasses import dataclass
from donnes_pipe.connector_interfaces import ConnectClient
from donnes_pipe.utils.helpers import make_request

@dataclass
class PublicAPIsClient(ConnectClient):
    name: str = "Public API Client"
    type: str = "api"
    API_URL = "https://api.publicapis.org"
    api: "PublicAPIsClient.Api" = None

    @contextmanager
    def connect(self):
        try:
            response = requests.get(self.API_URL + "/random")

            if response.status_code != 200:
                raise Exception(f"Connection failed to {self.name}")

            self.api = self.Api(url=self.API_URL)
            yield self
        except Exception as e:
            raise e

    @dataclass
    class Api:
        url: str

        def get_entries(self):
            return make_request(
                method="GET", url=self.url + "/entries"
            )