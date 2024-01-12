import logging
import os
from datetime import datetime


def get_root_logger(logger_name, filename=None):
    """get the logger object"""
    logger = logging.getLogger(logger_name)
    debug = os.environ.get("ENV", "development") == "development"
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if filename:
        # Add a timestamp to the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_with_timestamp = f"{filename}_{timestamp}.log"
        fh = logging.FileHandler(filename_with_timestamp)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def get_child_logger(root_logger, name):
    return logging.getLogger(".".join([root_logger, name]))


LOG_PATH = "logs"
logger = get_root_logger(__name__, filename=os.path.join(LOG_PATH, "output"))
