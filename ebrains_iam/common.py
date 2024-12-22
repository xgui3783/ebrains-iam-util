import re
from base64 import b64decode
import json

def camel_to_snake(input: str):
    return re.sub(r'([A-Z]+)', r'_\1', input).lower()

def decode_jwt(jwt_token: str):
    _header, body, _sig, *_rest = jwt_token.split('.')
    return tuple(
        json.loads(b64decode(v.encode("utf-8") + b"====").decode("utf-8"))
        for v in [_header, body]
    )
