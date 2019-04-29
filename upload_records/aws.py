import boto3


def get_api_token():
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(
        SecretId="gfw-api/prod-token"
    )
    return response["SecretString"]


def get_s3_records(bucket_name, prefix):

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(name=bucket_name)

    return bucket.objects.filter(Prefix=prefix)