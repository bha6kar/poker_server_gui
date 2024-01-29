import os
from datetime import datetime
from pathlib import Path

import structlog


def get_root_logger(logger_name, filename=None):
    """get the logger object"""
    logger = structlog.getLogger()

    # Add a timestamp to the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_with_timestamp = f"{filename}_{timestamp}"
    structlog.configure(
        processors=[
            # structlog.processors.add_log_level,
            # structlog.processors.StackInfoRenderer(),
            # structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            # structlog.processors.EventRenamer("msg"),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.WriteLoggerFactory(
            file=Path(filename_with_timestamp).with_suffix(".log").open("wt")
        ),
    )

    return logger


LOG_PATH = "logs"
logger = get_root_logger(__name__, filename=os.path.join(LOG_PATH, "output"))

if __name__ == "__main__":
    logger.info("Hi from logger.")
