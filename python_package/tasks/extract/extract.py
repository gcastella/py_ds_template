from python_package.tasks import BaseTask

import pandas as pd
import logging
from sklearn.datasets import load_iris

logger = logging.getLogger(__name__)


class ExtractTask(BaseTask):
    def __init__(self):
        super(ExtractTask, self).__init__("extract")

    def run(self):
        iris_df = self.extract()
        self.write(data=iris_df, file=self.output)

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
