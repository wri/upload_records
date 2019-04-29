import logging
import sys
from datetime import datetime
import os


def get_logfile(dataset):
    now = datetime.now()
    dirname = os.path.dirname(__file__)
    log_dir = os.path.join(dirname, "log")

    try:
        os.makedirs(log_dir)
    except FileExistsError:
        # directory already exists
        pass

    logfile = "{}/{}_{}.log".format(log_dir, dataset, datetime.strftime(now, "%Y%m%d-%H%M%S"))

    return logfile


def get_logger(logfile, debug=False):
    """
    Build logger
    :param logfile: Location of logfile
    :param debug: Set Log Level to Debug or Info
    :return: logger
    """

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    sh = logging.StreamHandler(sys.stdout)
    fh = logging.FileHandler(logfile)

    #sh.setLevel(logging.DEBUG)
    fh.setLevel(logging.INFO)

    sh.setFormatter(formatter)
    fh.setFormatter(formatter)

    root.addHandler(sh)
    root.addHandler(fh)

    return root