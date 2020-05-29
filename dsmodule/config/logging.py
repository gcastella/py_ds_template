import logging.config
import os

import yaml

from dsmodule.config import config


def load_logging(yaml_file=config.log_file, logs_dir=config.path.logs):
    os.makedirs(logs_dir, exist_ok=True)
    if os.path.exists(yaml_file):
        with open(yaml_file, "r") as file:
            log_config = yaml.safe_load(file)
        logging.config.dictConfig(log_config)
    else:
        raise FileNotFoundError(
            f"Log yaml configuration file not found in {yaml_file}"
        )
