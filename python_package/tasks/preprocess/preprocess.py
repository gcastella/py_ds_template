import pandas as pd
import logging
from pathlib import Path

from sklearn.decomposition import PCA
from python_package.config import config
from python_package.utils import add_version, get_from_module

logger = logging.getLogger(__name__)


class PreProcessTask:
    def __init__(self):
        # Reading relevant config
        self.paths = config.run.paths
        self.version = config.run.version
        self.loader = config.task.preprocess.loader
        self.writer = config.task.preprocess.writer
        self.input = str(
            Path(self.paths.source) /
            add_version(config.task.preprocess.input, self.version, end=False)
        )
        self.output = str(
            Path(self.paths.preprocess) /
            add_version(config.task.preprocess.output, self.version, end=False)
        )

        # Logging
        logger.info(
            f"Initiated PreProcessTask run with version {self.version}."
        )

    def run(self):
        data = self.load()
        pp_data = self.pre_process(data)
        self.write(pp_data)

    def load(self) -> pd.DataFrame:
        loader = get_from_module(self.loader.module, self.loader.name)
        data = loader(self.input, **self.loader.params)
        logger.info(f"Loaded data from {self.input}.")
        logger.debug(data.head(5))
        return data

    def write(self, data: pd.DataFrame) -> None:
        writer = get_from_module(self.writer.module, self.writer.name)
        writer(data, self.output, **self.writer.params)
        logger.debug(data.head(5))
        logger.info(f"Saved data in {self.input}.")

    def pre_process(self, data):
        col_names = list(data.columns)
        target = col_names[-1:]
        variables = col_names[:-1]

        pca = PCA(1)
        df_pca = pca.fit_transform(data[variables])

        df_pp = data.copy()
        df_pp["pca_comp1"] = df_pca[:, 0]
        logger.info(f"Added first PCA component.")
        logger.debug(df_pp.head(5))

        return df_pp
