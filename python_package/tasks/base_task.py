import pandas as pd
import logging
from pathlib import Path

from python_package.config import config
from python_package.utils import add_version, get_from_module

logger = logging.getLogger(__name__)


class BaseTask:
    def __init__(self, task_scope: str):
        """
        Init a task and get parameters for the run.

        Args:
            task_scope: string matching one of the labels in run
            configuration tasks and run paths in config.
        """
        # Reading relevant config
        self.scope = task_scope
        self.paths = config.run.paths
        self.version = config.run.version
        self.loader = config.task[task_scope].loader
        self.writer = config.task[task_scope].writer
        if config.task[task_scope].input:
            self.input = add_version(
                **config.task[task_scope].input,
                version=self.version,
                end=False
            )
        else:
            self.input = ""
            logger.info("No input file found in config.")
        if config.task[task_scope].output:
            self.output = add_version(
                **config.task[task_scope].output,
                version=self.version,
                end=False
            )
        else:
            self.output = ""
            logger.info("No output file found in config.")

        # Logging
        logger.info(
            f"Initiated {task_scope} task run with version {self.version}."
        )

    def run(self):
        """
        Actually runs all the task, usually load, do something,
        write back results.
        """
        pass

    def load(self, file: str) -> pd.DataFrame:
        """
        Load data from files to return a data frame
        """
        loader = get_from_module(self.loader.module, self.loader.name)
        data = loader(file, **self.loader.params)
        logger.info(f"Loaded data from {self.input}.")
        logger.debug(data.head(5))
        return data

    def write(self, data: pd.DataFrame, file: str) -> None:
        """
        Write data frame object.
        """
        writer = get_from_module(self.writer.module, self.writer.name)
        writer(data, file, **self.writer.params)
        logger.debug(data.head(5))
        logger.info(f"Saved data in {self.input}.")

    def get_scope(self):
        """
        Get scope of a task
        """
        return self.scope
