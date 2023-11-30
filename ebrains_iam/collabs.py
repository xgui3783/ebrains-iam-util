import requests
from dataclasses import dataclass
from typing import Literal
import sys

from .users import User
from .config import wiki_endpoint
from .common import camel_to_snake

TYPE_ROLE = Literal["administrator", "editor", "viewer"]
possible_roles = ("administrator", "editor", "viewer",)

@dataclass
class Collab:
    name: str
    title: str
    description: str
    is_public: bool
    is_member: bool
    has_drive: bool
    has_bucket: bool
    link: str
    create_date: int
    drive_repository_id: str
    nb_like: int
    owner: str

    @classmethod
    def from_json(cls, json_obj: dict):
        return cls(**{
            camel_to_snake(key): value
            for key, value in json_obj.items()
        })
    
    @property
    def base_url(self):
        return f"{wiki_endpoint}/rest/v1/collabs/{self.name}"
    
    def list_teams(self, role: TYPE_ROLE, *, token: str):
        assert role in possible_roles, f"{role=!r} must be in {possible_roles}"
        resp = requests.get(f"{self.base_url}/team/{role}", headers={
            "Authorization": f"bearer {token}"
        })
        resp.raise_for_status()
        users = resp.json().get("users", [])
        return {
            "users": [User.from_json(user) for user in users]
        }
        

    def add_team(self, username: str, role: TYPE_ROLE, *, is_service_account: bool=False, token: str):
        """Adding a user to this collab with the specified role
        
        Args:
            username: str username of the user. Can use OIDC client-id, but the is_service_account flag must be set to true
            role: str one of administrator, editor, viewer
            is_service_account: bool set if the username point to an OIDC client (for client credential flow)
            token: str bearer token needed to authenticate the request"""
        assert role in possible_roles, f"{role=!r} must be in {possible_roles}"

        if is_service_account:
            username = f"service-account-{username}"

        resp = requests.put(f"{self.base_url}/team/{role}/users/{username}", headers={
            "Authorization": f"bearer {token}"
        })
        resp.raise_for_status()
        print(f"Adding user {username} to collab {self.name} as role {role} successful!", file=sys.stderr)

    def remove_team(self, username: str, role: TYPE_ROLE, *, is_service_account: bool=False, token: str):
        """Removing a user to this collab with the specified role
        
        Args:
            username: str username of the user. Can use OIDC client-id, but the is_service_account flag must be set to true
            role: str one of administrator, editor, viewer
            is_service_account: bool set if the username point to an OIDC client (for client credential flow)
            token: str bearer token needed to authenticate the request"""
        assert role in possible_roles, f"{role=!r} must be in {possible_roles}"

        if is_service_account:
            username = f"service-account-{username}"

        resp = requests.delete(f"{self.base_url}/team/{role}/users/{username}", headers={
            "Authorization": f"bearer {token}"
        })
        resp.raise_for_status()
        print(f"Deleting user {username} from collab {self.name} as role {role} successful!", file=sys.stderr)


def get_collab(collab_id: str, *, token: str):
    resp = requests.get(f"{wiki_endpoint}/rest/v1/collabs/{collab_id}", headers={
        "Authorization": f"bearer {token}"
    })
    resp.raise_for_status()
    return Collab.from_json(resp.json())
    
