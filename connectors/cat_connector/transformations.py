from dataclasses import dataclass
from donnes_pipe.connector_interfaces import ConnectorTransformer

@dataclass
class CatTranformType1(ConnectorTransformer):
    description: str = "This will create a unique object with all breeds in one place"
    verison: str = "1.0"

    def apply(self, data):
        return data


@dataclass
class CatTranformType2(ConnectorTransformer):
    description: str = "This will create a unique object with all breeds in one place"
    verison: str = "1.0"

    def apply(self, data):
        return data


@dataclass
class CatTranformType3(ConnectorTransformer):
    description: str = (
        "this will join all the breeds in one place with a date of last year"
    )
    verison: str = "1.0"

    def apply(self, data):
        return data


def get_cat_api_transformers(transformer_name) -> ConnectorTransformer:
    factory = {
        "deafult": CatTranformType1,
        "type1": CatTranformType1,
        "type2": CatTranformType2,
        "type3": CatTranformType3,
    }

    if transformer_name not in factory:
        raise Exception(f"Unknown transformer: {transformer_name}")

    return factory[transformer_name]()
