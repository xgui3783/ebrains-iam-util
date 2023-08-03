import requests
from dataclasses import dataclass

from .config import auth_endpoint
from .exceptions import MalformedOIDCException

@dataclass
class OIDCEndpointConfig:
    token_endpoint: str
    device_authorization_endpoint: str


def init_config():
    resp = requests.get(f"{auth_endpoint}/.well-known/openid-configuration")
    resp.raise_for_status()
    json_resp = resp.json()
    try:
        assert "device_authorization_endpoint" in json_resp
        assert "token_endpoint" in json_resp
        return OIDCEndpointConfig(
            token_endpoint=json_resp.get("token_endpoint"),
            device_authorization_endpoint=json_resp.get("device_authorization_endpoint"),
        )
    except AssertionError as e:
        raise MalformedOIDCException from e
