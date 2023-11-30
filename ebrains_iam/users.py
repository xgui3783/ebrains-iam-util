from dataclasses import dataclass
import re

import requests

from .config import wiki_endpoint
from .common import camel_to_snake

@dataclass
class User:
    id: str
    mitre_id: str
    username: str
    first_name: str
    last_name: str
    email: str
    biography: str
    avatar: str
    active: bool

    @classmethod
    def from_json(cls, json_obj: dict):
        return cls(**{
            camel_to_snake(key): value
            for key, value in json_obj.items()
        })

# API according to https://wiki.ebrains.eu/bin/view/Collabs/the-collaboratory/Documentation%20Wiki/API/

def get_user(username: str, *, token: str):
    resp = requests.get(f"{wiki_endpoint}/rest/v1/identity/users/{username}", headers={
        "Authorization": f"bearer {token}"
    })
    resp.raise_for_status()
    return User.from_json(resp.json())
