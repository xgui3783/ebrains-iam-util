from typing import List
import requests
import json
from base64 import b64decode
import time

from .base import OIDCEndpointConfig, init_config

class ClientCredentialsSession:
    oidc_config:OIDCEndpointConfig=None

    def __init__(self, scope: List[str]=[]) -> None:
        from .config import cc_flow_client_id, cc_flow_client_secret
        if not self.oidc_config:
            self.__class__.oidc_config = init_config()
            self.oidc_config = self.__class__.oidc_config
        
        if not cc_flow_client_id or not cc_flow_client_secret:
            raise Exception(f"sa client id or sa client secret not set. cannot get s2s token")
        
        self.scope=scope
        self.s2s_token:str=None
        self.exp:float=None
        
        
    def refresh(self):
        from .config import cc_flow_client_id, cc_flow_client_secret
        token_endpoint = self.oidc_config.token_endpoint
        data={
            "client_id": cc_flow_client_id,
            "client_secret": cc_flow_client_secret,
            "grant_type": "client_credentials",
        }
        if self.scope:
            data["scope"] = "+".join(self.scope)

        resp = requests.post(token_endpoint, data=data)
        print(data, (cc_flow_client_id, cc_flow_client_secret))
        resp.raise_for_status()

        token = resp.json()
        auth_token = token.get("access_token")
        self.s2s_token = auth_token
        _header, body, _sig, *_rest = auth_token.split('.')
        self.exp = json.loads(b64decode(body.encode("utf-8") + b"====").decode("utf-8")).get("exp")

    def get_token(self):
        if self.s2s_token is None:
            self.refresh()
        diff = self.exp - time.time()
        # if the token is about to expire (30 seconds)
        if diff < 30:
            self.refresh()
        return self.s2s_token
