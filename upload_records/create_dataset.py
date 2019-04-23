from upload_records.utils import get_api_token
import requests
import click

@click.command()
@click.argument("dataset")
@click.option("dataset_name")
@click.option("connector")
def cli(dataset, dataset_name, connector):
        _create_record

        #https://gfw-files.s3.amazonaws.com/2018_update/results/dummydata.json

def _create_record(dataset, record):

    token = get_api_token()
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer {}".format(token)}
    r = requests.post("https://production-api.globalforestwatch.org/v1/dataset/{}/concat".format(dataset),
                      data={"url": record},
                      headers=headers)

    if r.status_code != 204:
        raise Exception("Data upload failed - received status code {}".format(r.status_code))