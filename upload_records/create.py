from upload_records.logger import get_logfile, get_logger
from upload_records.aws import get_api_token, get_s3_records
from upload_records.concatenate import concatenate_records
from upload_records.tasks import get_task_log, get_record_count
import click
import json
import logging
import requests
import os


@click.command()
@click.argument("dataset_name")
@click.argument("bucket")
@click.option("--prefix", default="/", help="Folder inside bucket containing records")
@click.option("--filetype", default="json")
def cli(dataset_name, bucket, prefix, filetype):

    get_logger(get_logfile(dataset_name))
    first = True
    dataset_id = None
    count = 0

    for obj in get_s3_records(bucket, prefix):
        s3_path = "https://{}.s3.amazonaws.com/{}".format(bucket, obj.key)

        filename, file_extension = os.path.splitext(s3_path)
        if file_extension == ".{}".format(filetype):
            if first:
                dataset_id = _create_dataset(dataset_name, s3_path)
                logging.info("Dataset ID: {}".format(dataset_id))
                get_task_log(dataset_id)
                new_count = get_record_count(dataset_id)
                logging.info("{} records added".format(new_count - count))
                count = new_count
                first = False
            else:
                count = concatenate_records(dataset_id, s3_path, filetype, count)


def _create_dataset(dataset_name, record):

    logging.info("Create dataset " + dataset_name)
    logging.info("Upload " + record)

    url = "https://production-api.globalforestwatch.org/v1/dataset/"

    token = json.loads(get_api_token())["token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    payload = {
        "connectorType": "document",
        "provider": "json",
        "connectorUrl": record,
        "name": dataset_name,
        "overwrite": True,
        "application": ["gfw"],
        "legend": {
            "nested": ["year_data"]
        },  # TODO: this should be hard coded. Find better way to pass in dataset attributes
    }

    r = requests.post(url, data=json.dumps(payload), headers=headers)

    if r.status_code != 200:
        raise Exception(
            "Data upload failed - received status code {}: "
            "Message: {}".format(r.status_code, r.json)
        )

    r_json = json.loads(r.text)
    dataset_id = r_json["data"]["id"]

    return dataset_id
