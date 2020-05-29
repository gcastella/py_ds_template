import logging

import click

from dsmodule.config import load_logging, config
from dsmodule.tasks.sample_tasks import (
    hello_world, get_config, start_version
)
from dsmodule.tasks.extract import ExtractTask
from dsmodule.tasks.preprocess import PreProcessTask
from dsmodule.tasks.train import TrainTask
from dsmodule.tasks.test import TestTask
from dsmodule.tasks.predict import PredictTask

logger = logging.getLogger(__name__)

# Lists of valid tasks and functions to use.
tasks = {
    "sample_task": hello_world,
    "get_config": get_config,
    "version": start_version,
    "extract": ExtractTask().run,
    "pre_process": PreProcessTask().run,
    "train": TrainTask().run,
    "test": TestTask().run,
    "predict": PredictTask().run,
}


def main(task):
    try:
        logger.debug(f"Task {task} started")
        tasks[task]()
    except:  # noqa
        logger.error(f"Task {task} failed")
        raise


@click.command()
@click.option(
    "--task",
    type=click.Choice(tasks.keys()),
    required=True,
    help="Name of task to execute",
)
def main_cli(task):
    load_logging()
    logger.info(f"Loaded general config from {config.config_file}")
    logger.info(f"Loaded logging config from {config.log_file}")
    logger.info(f"Loaded run config from {config.run_file}")
    main(task)
