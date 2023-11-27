from dataclasses import dataclass
from donnes_pipe.connector_interfaces import ConnectorTransformer

@dataclass
class PublicBasicInfoTransformation(ConnectorTransformer):
    description: str = "Get a basic information"
    version: str = "1.0"

    def get_basic_info(self, raw_data: list[dict]):
        result = []

        for data in raw_data:
            result.append({
                "name": data.get("API"),
                "description": data.get("Description"),
                "link": data.get("Link"),
            })

        return result