from upload_records.logger import get_logfile, get_logger
from upload_records.aws import get_api_token, get_s3_records
from upload_records.append import append_records
from upload_records.tasks import get_task_log, get_record_count
import click
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
@click.option("--env", default="production")
def cli(dataset_name, bucket, prefix, filetype, env):
    get_logger(get_logfile(dataset_name))
    first = True
    dataset_id = None
    count = 0

    for obj in get_s3_records(bucket, prefix):
        s3_path = "https://{}.s3.amazonaws.com/{}".format(bucket, obj.key)

        filename, file_extension = os.path.splitext(s3_path)
        if file_extension == ".{}".format(filetype):
            if first:
                dataset_id = _create_dataset(dataset_name, s3_path, env)
                logging.info("Dataset ID: {}".format(dataset_id))
                get_task_log(dataset_id, env)
                new_count = get_record_count(dataset_id, env)
                logging.info("{} records added".format(new_count - count))
                count = new_count
                first = False
            else:
                time.sleep(300)
                count = append_records(dataset_id, s3_path, filetype, count, env)


def _create_dataset(dataset_name, record, env="production"):
    logging.info("Create dataset " + dataset_name)
    logging.info("Upload " + record)

    url = "https://{}-api.globalforestwatch.org/v1/dataset/".format(env)

    token = get_api_token(env)

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
            "keyword": [
                "iso",
                "ifl",
                "tcs",
                "global_land_cover",
                "erosion",
                "wdpa",
                "plantations",
                "river_basin",
                "ecozone",
                "water_stress",
                "rspo",
                "idn_land_cover",
                "mex_forest_zoning",
                "per_forest_concession",
                "bra_biomes"
            ],
            "boolean": [
                "primary_forest",
                "idn_primary_forest",
                "biodiversity_significance",
                "biodiversity_intactness",
                "aze",
                "urban_watershed",
                "mangroves_1996",
                "mangroves_2016",
                "endemic_bird_area",
                "tiger_cl",
                "landmark",
                "land_right",
                "kba",
                "mining",
                "oil_palm",
                "idn_forest_moratorium",
                "mex_protected_areas",
                "mex_pes",
                "per_production_forest",
                "per_protected_area",
                "wood_fiber",
                "resource_right",
                "managed_forests",
                "oil_gas"
            ],
            "integer": [
                "threshold",
            ],
            "double": [
                "total_area",
                "extent_2000",
                "extent_2010",
                "total_gain",
                "total_biomass",
                "avg_biomass_per_ha",
                "total_co2",
                "total_mangrove_biomass",
                "avg_mangrove_biomass_per_ha",
                "total_mangrove_co2"
            ],
            "nested": ["year_data"]
        },  # TODO: this shouldn't be hard coded. Find better way to pass in dataset attributes
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


if __name__ == "__main__":
    cli()
