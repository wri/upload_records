from retrying import retry
import requests
import os
import json
import logging


@retry(wait_fixed=2000)
def get_task_log(dataset):

    url = "https://production-api.globalforestwatch.org/v1/dataset/{}".format(dataset)
    r = requests.get(url)
    r_json = json.loads(r.text)
    status = r_json["data"]["attributes"]["status"]

    if status == "saved":
        task_id = r_json["data"]["attributes"]["taskId"]
        url = os.path.join("https://production-api.globalforestwatch.org" + task_id)
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

    else:
        raise Exception("Dataset not saved")


def get_record_count(dataset):
    url = "https://production-api.globalforestwatch.org/v1/query/{}?sql=select count(*) from table".format(
        dataset
    )
    r = requests.get(url)
    r_json = json.loads(r.text)
    count = r_json["data"][0]["COUNT(*)"]
    logging.info("Number of records: {}".format(count))
    return count
