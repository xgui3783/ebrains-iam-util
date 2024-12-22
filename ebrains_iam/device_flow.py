from typing import List
import requests
from time import sleep

from .exceptions import AuthError
from .base import init_config

def _parse_client_id(client_id: str=None):
    
    from .config import client_id as env_client_id
    client_id = client_id or env_client_id
    assert client_id, "client id must be provided, either via envvar EBRAINS_CLIENT_ID (default: siibra), or passed in as argument"
    return client_id


def refresh(refresh_token: str, client_id: str=None):
    return refresh_raw(refresh_token, client_id).get("access_token")

def refresh_raw(refresh_token: str, client_id: str=None):

    client_id = _parse_client_id(client_id)

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


def start(scope:List[str]=[], client_id: str=None) -> str:
    return start_raw(scope, client_id=client_id).get("access_token")

def start_raw(scope:List[str]=None, client_id: str=None) -> dict:
    from .config import polling_interval, max_retries

    client_id = _parse_client_id(client_id)
    scope = scope or []

    config = init_config()

    data={
        "client_id": client_id
    }
    if scope:
        assert isinstance(scope, list)
        assert all(isinstance(item, str) for item in scope)
            # scope is space delimited
            # see https://datatracker.ietf.org/doc/html/rfc8628#section-3.1
        data["scope"]=" ".join(scope)
    
    resp = requests.post(url=config.device_authorization_endpoint, data=data)
    resp.raise_for_status()
    resp_json = resp.json()
    
    assert "verification_uri_complete" in resp_json
    assert "device_code" in resp_json

    device_code = resp_json.get("device_code")

    print("***")
    print(f"To continue, please go to {resp_json.get('verification_uri_complete')}")
    print("***")
    
    attempt_number = 0
    sleep_timer = polling_interval
    while True:
        # TODO the polling is a little busted at the moment.
        # need to speak to axel to shorten the polling duration
        sleep(sleep_timer)

        if attempt_number > max_retries:
            message = (
                f"exceeded max attempts: {max_retries}, aborting..."
            )
            raise AuthError(message)
        attempt_number += 1
        resp = requests.post(
            url=config.token_endpoint,
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "client_id": client_id,
                "device_code": device_code,
            },
        )

        if resp.status_code == 200:
            json_resp = resp.json()
            return json_resp

        if resp.status_code == 400:
            json_resp = resp.json()
            error = json_resp.get("error")
            if error == "slow_down":
                sleep_timer += 1
            continue

