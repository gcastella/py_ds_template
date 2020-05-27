import logging
import pandas as pd

from python_package.config import config
from python_package.utils import add_version, get_from_module
from python_package.tasks import BaseTask

logger = logging.getLogger(__name__)


class TestTask(BaseTask):
    def __init__(self):
        super(TestTask, self).__init__("test")
        self.input_split = add_version(
            **config.task[self.scope].input_split,
            version=self.version,
            end=False
        )
        self.input_model = add_version(
            **config.task[self.scope].input_model,
            version=self.version,
            end=False
        )

    def run(self):
        # Load model and data
        model = self.load(file=self.input_model)
        split_data = self.load(file=self.input_split)

        # Evaluate model
        df_score = self.test(model, **split_data)

        # Save scores
        self.write(data=df_score, file=self.output)

    def test(self, model, X_train, X_test, y_train, y_test):
        score_list = []
        for metric, fun_config in self.task_config.metrics.items():
            logger.info(f"Calculating '{metric}' score.")
            score_fun = get_from_module(fun_config.module, fun_config.name)
            score_row = dict()
            score_row["metric"] = metric
            score_row["train_score"] = \
                score_fun(
                    y_pred=model.predict(X_train),
                    y_true=y_train,
                    **fun_config.params
                )
            score_row["test_score"] = \
                score_fun(
                    y_pred=model.predict(X_test),
                    y_true=y_test,
                    **fun_config.params
                )
            score_list.append(score_row)
        df_score = pd.DataFrame(score_list)
        logger.info("All metrics have been calculated.")
        logger.debug(df_score.head())
        return df_score
