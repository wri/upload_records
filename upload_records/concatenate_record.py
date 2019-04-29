from retrying import retry
from upload_records.utils import get_api_token
from datetime import datetime
import boto3
import requests
import click
import os
import json
import logging

TOKEN = json.loads(get_api_token())["token"]


@click.command()
@click.argument("dataset")
@click.argument("bucket")
@click.option("--prefix", default="/", help="Folder inside bucket containing records")
@click.option("--filetype", default="json")
def cli(dataset, bucket, prefix, filetype):

    logger = _get_logger(dataset)

    for obj in _get_s3_records(bucket, prefix):
        s3_path = "https://{}.s3.amazonaws.com/{}".format(bucket, obj.key)
        filename, file_extension = os.path.splitext(s3_path)
        if file_extension == ".{}".format(filetype):
            logger.info("upload " + s3_path)
            _concatenate_record(dataset, s3_path)


def _get_logger(dataset):

    now = datetime.now()

    if not os.path.exists("log"):
        os.makedirs("log")

    logger = logging.getLogger("concatenate_records")
    hdlr = logging.FileHandler("log/{}_{}.log".format(dataset, datetime.strftime(now, "%Y%m%d-%H%M%S")))
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    return logger

def _get_s3_records(bucket_name, prefix):

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(name=bucket_name)

    return bucket.objects.filter(Prefix=prefix)


@retry(wait_fixed=2000)
def _concatenate_record(dataset, record):

    click.echo("Concatenate record " + record)

    url = "https://production-api.globalforestwatch.org/v1/dataset/{}/concat".format(dataset)

    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer {}".format(TOKEN)
             }

    payload = {"connectorType": "document",
                "provider": "json",
                "url": record}

    r = requests.post(url,
                      data=json.dumps(payload),
                      headers=headers)

    click.echo(r.text)

    if r.status_code != 204:
        raise Exception("Data upload failed - received status code {}: "\
                        "Message: {}".format(r.status_code, r.json))




