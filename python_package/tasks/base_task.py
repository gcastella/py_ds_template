import pandas as pd
import logging
from typing import Dict, Any, Callable

from python_package.config import config
from python_package.utils import add_version, get_from_module, func_def

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
        self.version = config.run.version
        self.config = config.task[task_scope]

        self.input = self.prepare_loaders()
        self.output = self.prepare_writers()

        # Logging
        logger.info(
            f"Initiated {task_scope} task run with version {self.version}."
        )

    @staticmethod
    def load(file: str, loader: Callable) -> Any:
        """Load data from files to return a data frame"""
        data = loader(file)
        logger.info(f"Loaded data from {file}.")
        return data

    @staticmethod
    def write(data: Any, file: str, writer: Callable) -> None:
        """Write data frame or model object to a file."""
        writer(data, file)
        logger.info(f"Saved data in {file}.")

    def get_scope(self) -> str:
        """Get scope of a task"""
        return self.scope

    def file_version(self, **location):
        """Returns the complete file path with the version."""
        return add_version(
            file=location["name"],
            path=location["path"],
            version=self.version,
            end=False,
        )

    def prepare_loaders(self) -> Dict[Dict[str, Callable]]:
        """
        Returns a dictionary of all functions used to
        load inputs and the input files to use.
        """
        loaders = dict()
        if self.config.input:
            for name, input in self.config.input.items():
                loader = func_def(**input.loader)
                file = self.file_version(**input.location)
                loaders[name] = {"file": file, "loader": loader}
        logger.debug("Prepared loaders.")
        return loaders

    def prepare_writers(self) -> Dict[Dict[str, Callable]]:
        """
        Returns a dictionary of all functions used to
        write outputs and the output files to use.
        """
        writers = dict()
        if self.config.output:
            for name, output in self.config.output.items():
                writer = func_def(**output.writer)
                file = self.file_version(**output.location)
                writers[name] = {"file": file, "writer": writer}
        logger.debug("Prepared writers.")
        return writers

    def run(self) -> None:
        """
        Actually runs all the task, usually load, do something,
        write back results.
        """
        logger.info("Replace 'run' method when inheriting from 'BaseTask'.")
