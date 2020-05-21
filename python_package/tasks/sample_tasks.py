import logging
import pprint

from python_package.config import config

logger = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)


def get_config():
    logger.info(f"Config file used was {config.config_file}")
    pp.pprint(config)


def hello_world():
    print("Printing Hello world!")
    logger.info("Log info Hello world!")
    logger.debug("Log debug Hello world!")
    logger.warning("Log warning Hello world!")
    logger.error("Log error Hello world!")
