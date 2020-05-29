import os

import yaml
from box import Box
from dotenv import load_dotenv

from dsmodule.utils import get_from_module


def box_yaml(file: str) -> Box:
    """
    Load yaml file and Box it.

    Args:
        file: path to yaml file.

    Returns:
        boxed yaml file.
    """
    with open(file, "r") as yml_file:
        cfg = Box(
            yaml.safe_load(yml_file),
            default_box=True,
            default_box_attr=None
        )
    return cfg


# Adding .env variables to environment
load_dotenv(dotenv_path=".env")

# Read .env variables.
ENV = os.getenv("ENVIRONMENT", "dev")
CONFIG_FILE = os.getenv("CONFIG_FILE")
RUN_FILE = os.getenv("RUN_FILE")
LOG_FILE = os.getenv("LOG_FILE")

# Build config object.
full_config = box_yaml(CONFIG_FILE)
run_config = box_yaml(RUN_FILE)
config = Box({
    **full_config["base"],
    **full_config[ENV],
    **run_config
}, default_box=True, default_box_attr=None)
config.environment = ENV
config.config_file = CONFIG_FILE
config.run_file = RUN_FILE
config.log_file = LOG_FILE

# Version
if config.run.use_existing_run:
    config.run.version = config.run.use_existing_run
else:
    config.run.version = get_from_module(**config.run.versioning)()
