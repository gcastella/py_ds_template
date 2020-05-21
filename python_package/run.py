import logging

import click

from python_package.config import load_logging, config
from python_package.tasks.sample_tasks import hello_world, get_config

logger = logging.getLogger(__name__)

# Lists of valid tasks and functions to use.
tasks = {
    "sample_task": hello_world,
    "get_config": get_config,
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
