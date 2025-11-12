import os
import json
import logging
import urllib3
import boto3
from botocore.exceptions import ClientError
from typing import Tuple

# ---------------------------------------------------------------------
# SAFE LOGGER SETUP
# ---------------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------------------------------------------------------------
# ENVIRONMENT VARIABLES (non-sensitive)
# ---------------------------------------------------------------------
SPLUNK_HEC_URL = os.getenv("SPLUNK_HEC_URL", "")
SPLUNK_INDEX   = os.getenv("SPLUNK_INDEX", "default")
SECRET_NAME    = os.getenv("SECRET_NAME", "log-ingest/app-name")
AWS_REGION     = os.getenv("AWS_REGION", "eu-west-1")

http = urllib3.PoolManager()

# ---------------------------------------------------------------------
# FETCH SECRETS SECURELY FROM SECRETS MANAGER
# ---------------------------------------------------------------------
def get_secret() -> Tuple[str, str]:
    """
    Retrieves and parses credentials stored in Secrets Manager.

    Returns:
        A tuple (splunk_hec_token, app_api_key)
    """
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=AWS_REGION)

    try:
        resp = client.get_secret_value(SecretId=SECRET_NAME)
    except ClientError as e:
        logger.error("Failed to retrieve secret: %s", e)
        raise

    secret_str = resp.get("SecretString", "{}")
    secret_json = json.loads(secret_str)

    # Extract credentials (do NOT log these)
    hec_token = secret_json["hectoken"]
    app_api_key = secret_json["app_api_key"]
    return hec_token, app_api_key


# ---------------------------------------------------------------------
# LAMBDA ENTRY POINT
# ---------------------------------------------------------------------
def lambda_handler(event, context):
    """
    Main Lambda function:
    1. Fetch secrets
    2. Optionally pull logs from an external API
    3. Forward events to Splunk HEC
    """

    HEC_TOKEN, APP_API_KEY = get_secret()
    logger.info("Function started in region=%s, index=%s", AWS_REGION, SPLUNK_INDEX)

    # --- Example placeholder for calling an external API ---
    # api_url = "https://api.example.com/logs"
    # response = http.request(
    #     "GET",
    #     api_url,
    #     headers={"Authorization": f"Bearer {APP_API_KEY}"},
    #     timeout=urllib3.Timeout(connect=5.0, read=30.0),
    # )
    # logger.info("Fetched logs, status=%s", response.status)

    # --- Example placeholder for sending to Splunk ---
    # payload = {"event": {"sample": "data"}, "index": SPLUNK_INDEX}
    # http.request(
    #     "POST",
    #     SPLUNK_HEC_URL,
    #     headers={"Authorization": f"Splunk {HEC_TOKEN}"},
    #     body=json.dumps(payload).encode("utf-8")
    # )

    return {"statusCode": 200, "body": json.dumps("Execution completed successfully")}
