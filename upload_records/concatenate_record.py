from retrying import retry
from upload_records.utils import get_api_token, get_logfile, get_logger
from datetime import datetime
import boto3
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

    for obj in _get_s3_records(bucket, prefix):
        s3_path = "https://{}.s3.amazonaws.com/{}".format(bucket, obj.key)
        filename, file_extension = os.path.splitext(s3_path)
        if file_extension == ".{}".format(filetype):
            _get_task_log(dataset)
            logging.info("Upload " + s3_path)
            _concatenate_record(dataset, s3_path)
            time.sleep(2) #give API some time to update status

    _get_task_log(dataset)


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


def _get_record_count(dataset):
    url = "https://production-api.globalforestwatch.org/v1/query/{}?sql=select count(*) from table".format(dataset)
    r = requests.get(url)
    r_json = json.loads(r.text)
    count = r_json["data"][0]["COUNT(*)"]
    logging.info("Number of records: {}".format(count))


@retry(wait_fixed=2000)
def _get_task_log(dataset):

    url = "https://production-api.globalforestwatch.org/v1/dataset/{}".format(dataset)
    r = requests.get(url)
    r_json = json.loads(r.text)
    status = r_json["data"]["attributes"]["status"]

    if status == "saved":
        _get_record_count(dataset)
        task_id = r_json["data"]["attributes"]["taskId"]
        url = os.path.join("https://production-api.globalforestwatch.org" + task_id)
        r = requests.get(url)
        r_json = json.loads(r.text)
        logs = r_json["data"]["attributes"]["logs"]
        for log in logs:
            if "withErrors" in log.keys() and log["withErrors"]:
                logging.error(r_json["data"]["attributes"]["message"]["fileUrl"] + ": " + log["detail"])
            if "error" in log.keys():
                logging.error(r_json["data"]["attributes"]["message"]["fileUrl"] + ": " + log["error"])

    else:
        raise Exception("Dataset not saved")


@retry(wait_fixed=2000)
def _concatenate_record(dataset, record):

    #_get_task_log(dataset)
    logging.debug("Concatenate record " + record)

    url = "https://production-api.globalforestwatch.org/v1/dataset/{}/concat".format(dataset)
    token = json.loads(get_api_token())["token"]

    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer {}".format(token)
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


if __name__ == "__main__":
    cli()