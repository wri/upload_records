from retrying import retry
from upload_records.logger import get_logfile, get_logger
from upload_records.aws import get_api_token, get_s3_records
from upload_records.tasks import get_record_count, get_task_log
import requests
import click
import os
import json
import logging
import time


@click.command()
@click.argument("dataset")
@click.argument("bucket")
@click.option("--prefix", default="/", help="Folder inside bucket containing records")
@click.option("--filetype", default="json")
def cli(dataset, bucket, prefix, filetype):

    get_logger(get_logfile(dataset))
    count = get_record_count(dataset)

    for obj in get_s3_records(bucket, prefix):
        s3_path = "https://{}.s3.amazonaws.com/{}".format(bucket, obj.key)
        count = concatenate_records(dataset, s3_path, filetype, count)


def concatenate_records(dataset, file_url, filetype, count=0):

    filename, file_extension = os.path.splitext(file_url)
    if file_extension == ".{}".format(filetype):
        logging.info("Upload " + file_url)
        _concatenate_records(dataset, file_url)
        time.sleep(5)  # Give API some time to update status
        get_task_log(dataset)
        new_count = get_record_count(dataset)
        logging.info("{} records added".format(new_count - count))

        return new_count

    else:
        return count


@retry(wait_fixed=2000)
def _concatenate_records(dataset, record):

    logging.debug("Concatenate record " + record)

    url = "https://production-api.globalforestwatch.org/v1/dataset/{}/concat".format(
        dataset
    )
    token = json.loads(get_api_token())["token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    payload = {"connectorType": "document", "provider": "json", "url": record}

    r = requests.post(url, data=json.dumps(payload), headers=headers)

    logging.debug(r.text)

    if r.status_code != 204:
        raise Exception(
            "Data upload failed - received status code {}: "
            "Message: {}".format(r.status_code, r.json)
        )


if __name__ == "__main__":
    cli()
