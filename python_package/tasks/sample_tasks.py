import logging

from python_package.config import config
from python_package.utils import get_from_module

logger = logging.getLogger(__name__)


def get_config():
    logger.info(f"Config file used was {config.config_file}")
    logger.debug(str(config))


def hello_world():
    print("Printing Hello world!")
    logger.info("Log info Hello world!")
    logger.debug("Log debug Hello world!")
    logger.warning("Log warning Hello world!")
    logger.error("Log error Hello world!")


def start_version():
    versioner = get_from_module(**config.run.versioning)
    version = versioner()
    logger.info(f"Use this version for the next runs: {version}.")
