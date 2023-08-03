import os

auth_endpoint = os.getenv("EBRAINS_AUTH_ENDPOINT", "https://iam.ebrains.eu/auth/realms/hbp")
client_id=os.getenv("EBRAINS_CLIENT_ID", "siibra")


polling_interval=float(os.getenv("EBRAINS_POLLING_INTERVAL", "5"))
max_retries=int(os.getenv("EBRAINS_POLLING_MAX_RETRIES", "12"))

cc_flow_client_id=os.getenv("EBRAINS_CCFLOW_CLIENT_ID")
cc_flow_client_secret=os.getenv("EBRAINS_CCFLOW_CLIENT_SECRET")
