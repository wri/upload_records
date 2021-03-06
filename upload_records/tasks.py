from retrying import retry
import requests
import json
import logging
from upload_records.errors import DatasetFailedError, DatasetPendingError


def retry_if_pending(exception):
    """Return True if we should retry
    In this case if the dataset is still pending
    or if the gateway times out and returns an expected results which usually causes a KeyError or a JSONDecodeError"""
    return isinstance(exception, (DatasetPendingError, KeyError, json.decoder.JSONDecodeError))


@retry(retry_on_exception=retry_if_pending, wait_fixed=2000)
def get_task_log(dataset, env="production"):

    url = "https://{}-api.globalforestwatch.org/v1/dataset/{}".format(env, dataset)
    r = requests.get(url)
    r_json = json.loads(r.text)
    status = r_json["data"]["attributes"]["status"]

    if status == "saved":
        task_id = r_json["data"]["attributes"]["taskId"]
        url = "https://{}-api.globalforestwatch.org{}".format(env, task_id)
        logging.info("Task: " + url)
        r = requests.get(url)
        r_json = json.loads(r.text)
        logs = r_json["data"]["attributes"]["logs"]
        for log in logs:
            if "withErrors" in log.keys() and log["withErrors"]:
                logging.error(
                    r_json["data"]["attributes"]["message"]["fileUrl"]
                    + ": "
                    + log["detail"]
                )
            if "error" in log.keys():
                logging.error(
                    r_json["data"]["attributes"]["message"]["fileUrl"]
                    + ": "
                    + log["error"]
                )
    elif status == "failed":
        raise DatasetFailedError("Dataset upload failed.")
    elif status == "pending":
        raise DatasetPendingError("Dataset still pending.")
    else:
        raise Exception("Dataset in unknown state: " + status)


@retry(wait_fixed=2000)
def get_record_count(dataset, env="production"):
    url = "https://{}-api.globalforestwatch.org/v1/query/{}?sql=select count(*) from table".format(
        env, dataset
    )
    r = requests.get(url)
    r_json = json.loads(r.text)
    count = r_json["data"][0]["COUNT(*)"]
    logging.info("Number of records: {}".format(count))
    return count

