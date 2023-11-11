from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class ConnectClient(ABC):
    name: str = None
    type: str = None
    config: dict = field(default_factory=dict)

    @abstractmethod
    def connect(self):
        pass


@dataclass
class ConnectorTransformer(ABC):
    description: str = "Hepl text to description that you need to apply"
    verison: str = "1.0"

    @abstractmethod
    def apply(self, data):
        pass


@dataclass
class ConnectorELT(ABC):
    @abstractmethod
    def extract_data(self, source_client: ConnectClient):
        pass

    @abstractmethod
    def transform_data(self):
        pass

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def run(self):
        pass
