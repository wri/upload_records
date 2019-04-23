import boto3


def get_api_token():
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(
        SecretId="gfw-api/prod-token"
    )
    return response["SecretString"]