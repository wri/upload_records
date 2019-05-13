import boto3
import json


def get_api_token(env):
    client = boto3.client("secretsmanager", region_name="us-east-1")

    if env == "production":
        env = "prod"
    else:
        env = "staging"

    response = client.get_secret_value(
        SecretId="gfw-api/{}-token".format(env)
    )
    return json.loads(response["SecretString"])["token"]


def get_s3_records(bucket_name, prefix):

    s3 = boto3.resource("s3", region_name="us-east-1")
    bucket = s3.Bucket(name=bucket_name)

    return bucket.objects.filter(Prefix=prefix)