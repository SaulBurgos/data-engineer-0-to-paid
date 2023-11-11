import json
from typing import Any
import requests

def make_request(method: str, url: str, **kwargs) -> Any:
    response = None
    try:
        response = requests.request(method, url, **kwargs)
        return response.json()
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {str(e)} || Server response: {response.text}")
        return response
    except Exception as e:
        print(f"Error on request: {str(e)}")
        return response
