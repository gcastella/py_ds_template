import logging
import pandas as pd

from python_package.config import config
from python_package.utils import add_version, get_from_module
from python_package.tasks import BaseTask

logger = logging.getLogger(__name__)


class TrainTask(BaseTask):
    def __init__(self):
        super(TrainTask, self).__init__("train")

    def run(self):
        # Load data
        data = self.load(**self.input["data"])

        # Separate into train and test data
        split_data = self.split(
            data=data,
            target=self.config.pipeline.target
        )

        # Save split
        self.write(data=split_data, **self.output["split"])

        # Train model
        model = self.train(**split_data)

        # Save model
        self.write(data=model, **self.output["model"])

    def split(self, data: pd.DataFrame, target: str):
        X = data.drop([target], axis=1)
        y = data[target]
        logger.debug(X.head())
        logger.debug(y.head())

        splitter = get_from_module(
            self.config.split.module,
            self.config.split.name
        )

        X_train, X_test, y_train, y_test = \
            splitter(X, y, **self.config.split.params)

        split_data = {
            "X_train": X_train, "X_test": X_test,
            "y_train": y_train, "y_test": y_test
        }

        logger.debug(split_data.keys())
        logger.info("The dataset was split into X_train, X_test, y_train and y_test.")  # noqa
        return split_data

    def train(self, X_train, X_test, y_train, y_test):
        model_func = get_from_module(
            self.config.model.module,
            self.config.model.name
        )
        model = model_func(**self.config.model.params)
        model.fit(X=X_train, y=y_train)
        logger.info("Model was fit with training data.")
        logger.info(f"train score: {model.score(X_train, y_train)}")
        logger.info(f"test score: {model.score(X_test, y_test)}")
        return model
