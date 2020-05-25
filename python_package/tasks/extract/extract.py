from python_package.config import config
from python_package.utils import add_version, get_from_module

from pathlib import Path
from pandas import pd
import logging
from sklearn.datasets import load_iris

logger = logging.getLogger(__name__)


class ExtractTask:
    def __init__(self):
        # Reading relevant config
        self.paths = config.run.paths
        self.version = config.run.version
        self.loader = None
        self.writer = config.task.extract.writer
        self.input = None
        self.output = str(
            Path(self.paths.source) /
            add_version(config.task.extract.output, self.version, end=False)
        )

        # Logging
        logger.info(
            f"Initiated PreProcessTask run with version {self.version}."
        )

    def run(self):
        iris_df = self.extract()
        self.write(iris_df)

    def write(self, data: pd.DataFrame) -> None:
        writer = get_from_module(self.writer.module, self.writer.name)
        writer(data, self.output, **self.writer.params)
        logger.debug(data.head(5))
        logger.info(f"Saved data in {self.input}.")

    def extract(self):
        iris = load_iris()
        columns = ["sepal_length", "sepal_width",
                   "petal_length", "petal_width",
                   "species"]
        df = pd.concat([
            pd.DataFrame(iris.data, columns=columns[:-1]),
            pd.DataFrame(iris.target_names[iris.target], columns=columns[-1:]),
            ],
            axis=1
        )

        logger.info(f"Loaded Iris data set.")
        return df
