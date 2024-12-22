import requests
from .base import init_config
from datetime import datetime
from .common import decode_jwt

threshold_seconds = 300 # 5 min

def refresh(refresh_token: str, client_id: str=None):

    from .config import client_id as env_client_id
    client_id = client_id or env_client_id
    assert client_id, "client id must be provided, either via envvar EBRAINS_CLIENT_ID (default: siibra), or passed in as argument"

    config = init_config()
    resp = requests.post(
        url=config.token_endpoint,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
        },
    )
    resp.raise_for_status()
    resp_json = resp.json()
    return resp_json

def smart_refresh(access_token: str, refresh_token: str, client_id: str=None):
    """Will only try to refresh if access token is less than 5 minute to expiration"""
    
    _header, body, *_ = decode_jwt(access_token)

    expiry = datetime.fromtimestamp(body.get("exp"))

    current = datetime.now()
    if (
        expiry > current
        and
        (expiry - current).seconds > threshold_seconds
    ):
        return access_token, refresh_token, False
    
    resp_json = refresh(refresh_token, client_id)
    return resp_json.get("access_token"), resp_json.get("refresh_token"), True
