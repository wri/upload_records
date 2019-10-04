from upload_records.logger import get_logfile, get_logger
from upload_records.aws import get_api_token, get_s3_records
from upload_records.append import append_records
from upload_records.tasks import get_task_log, get_record_count
import upload_records.schemas as schemas
import boto3
import click
import importlib
import json
import logging
import requests
import os
import time


@click.command()
@click.argument("dataset_name")
@click.argument("bucket")
@click.option("--prefix", default="/", help="Folder inside bucket containing records")
@click.option("--filetype", default="json")
@click.option("--schema", default="annualupdate_iso")
@click.option("--env", default="production")
def cli(dataset_name, bucket, prefix, filetype, schema, env):
    get_logger(get_logfile(dataset_name))
    # first = True
    dataset_id = None
    count = 0

    legend_schema = getattr(schemas, schema)

    records = list()
    for obj in get_s3_records(bucket, prefix):

        s3_path = "https://{}.s3.amazonaws.com/{}".format(bucket, obj.key)

        filename, file_extension = os.path.splitext(s3_path)
        if file_extension == ".{}".format(filetype) and obj.size > 3:
            records.append(s3_path)

    dataset_id = _create_dataset(dataset_name, records, legend_schema, env)
    logging.info("Dataset ID: {}".format(dataset_id))
    get_task_log(dataset_id, env)
    new_count = get_record_count(dataset_id, env)
    logging.info("{} records added".format(new_count - count))


def _create_dataset(dataset_name, records, schema, env="production"):
    logging.info("Create dataset " + dataset_name)
    logging.info("Upload " + str(records))

    url = "https://{}-api.globalforestwatch.org/v1/dataset/".format(env)

    token = get_api_token(env)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    payload = {
        "connectorType": "document",
        "provider": "tsv",
        # "connectorUrl": record,
        "sources": records,
        "name": dataset_name,
        "overwrite": True,
        "application": ["gfw"],
        "legend": schema,
    }

    r = requests.post(url, data=json.dumps(payload), headers=headers)

    if r.status_code != 200:
        raise Exception(
            "Data upload failed - received status code {}: "
            "Message: {}".format(r.status_code, r.text)
        )

    r_json = json.loads(r.text)
    dataset_id = r_json["data"]["id"]

    return dataset_id


if __name__ == "__main__":
    cli()
