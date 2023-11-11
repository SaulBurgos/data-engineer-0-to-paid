from dataclasses import dataclass
from donnes_pipe.connector_interfaces import ConnectorTransformer

@dataclass
class CatBasicInfoTransformation(ConnectorTransformer):
    description: str = "Get a basic breed information"
    version: str = "1.0"

    def get_info(self, raw_data: list[dict]) -> list[dict]:
        results = []

        for item in raw_data:
            results.append({
                "id": item.get('id'),
                "name": item.get('name'),
                "temperament": item.get('temperament'),
                "origin": item.get('origin'),
                "description": item.get('description'),
                "origin": item.get('origin'),
                "wiki_url": item.get('wikipedia_url'),
                "image": item.get('image')
            })

        return results
    
    def mark_social_and_inteligent_cats(self, breeds_info: list[dict]) -> list[dict]:

        for item in breeds_info:
            temperament_list = [ s.strip().lower() for s in item.get('temperament').split(",")]

            if "social" in temperament_list:
                item.update({"is_social": True})

            if "intelligent" in temperament_list:
                item.update({"is_intelligent": True})
                
        return breeds_info


def get_cat_api_transformers(transformer_name) -> ConnectorTransformer:
    factory = {
        "basic_info": CatBasicInfoTransformation
    }

    if transformer_name not in factory:
        raise Exception(f"Unknown transformer: {transformer_name}")

    return factory[transformer_name]()
