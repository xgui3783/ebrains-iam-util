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

Getting service 2 service token (via client credential)

```python
import os

os.environ["EBRAINS_CCFLOW_CLIENT_ID"] = "your-client-id"
os.environ["EBRAINS_CCFLOW_CLIENT_SECRET"] = "your-client-secret"

from ebrains_iam.client_credential import ClientCredentialsSession

sess = ClientCredentialsSession(scope=["team"])
token = sess.get_token()
```

## License

MIT
