# EBRAINS IAM utility

Utility library that helps fetching a valid token. 

## Example

Getting a personal token via device flow

```python
import os

os.environ["EBRAINS_CLIENT_ID"] = "your-client-id-supporting-device-flow" # default value: `siibra`

from ebrains_iam.device_flow import start

# Get a token with additional team scope
token = start(scope=["team"])
```

Getting long lived (offline) token

```python
from ebrains_iam.device_flow import start_raw
from ebrains_iam.refresh import smart_refresh
import time

# offline scope is required for this to work
scopes = ["offline", "team", "openid"]

tokens = start_raw(scopes)
access_token = tokens.get("access_token")
refresh_token = tokens.get("refresh_token")

fuse = 120
while True:
    if fuse < 0:
        break
    access_token, refresh_token, flag = smart_refresh(access_token, refresh_token)
    if flag:
        print("Token refreshed")
    
    fuse -= 1
    time.sleep(60)

```

Getting service 2 service token (via client credential)

```python
import os

os.environ["EBRAINS_CCFLOW_CLIENT_ID"] = "your-client-id"
os.environ["EBRAINS_CCFLOW_CLIENT_SECRET"] = "your-client-secret"

from ebrains_iam.client_credential import ClientCredentialsSession

sess = ClientCredentialsSession(scope=["team"])
token = sess.get_token()
```

or provide the token on construction time (env var will be ignored if supplied)

```python
from ebrains_iam.client_credential import ClientCredentialsSession

sess = ClientCredentialsSession("your_client_id_2", "your_client_secret_2", scope=["team"])
token = sess.get_token()
```

## License

MIT
