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

@dataclass
class ConnectorELT(ABC):

     # non-abstract method
    def extract_data(self, source_client: ConnectClient):
        pass

    # non-abstract method
    def transform_data(self):
        pass

    # non-abstract method
    def load_data(self):
        pass

    # non-abstract method
    def run(self):
        pass
