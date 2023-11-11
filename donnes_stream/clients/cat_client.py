import requests
from contextlib import contextmanager
from dataclasses import dataclass, field
from donnes_stream.connector_interfaces import ConnectorELT, ConnectClient, ConnectorTransformer
from donnes_stream.utils.helpers import make_request

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
            response = requests.get(self.API_URL + "/images/search", headers=self.headers)

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
