import logging
import pandas as pd

from dsmodule.tasks import BaseTask
from dsmodule.tasks.preprocess import PreProcessTask

logger = logging.getLogger(__name__)


class PredictTask(BaseTask):
    def __init__(self):
        super(PredictTask, self).__init__("predict")

    def run(self):
        # Load data and model
        data = self.load(**self.input["predict_data"])
        model = self.load(**self.input["model"])
        preprocess = self.load(**self.input["preprocess"])

        # Preprocess data
        pp_data = self.preprocess(data, preprocess)

        # Predict labels
        y_pred = self.predict(data=pp_data, model=model)

        # Save predictions
        self.write(data=y_pred, **self.output["predictions"])

    @staticmethod
    def predict(data: pd.DataFrame, model) -> pd.DataFrame:
        y_pred = pd.DataFrame(model.predict(data))
        return y_pred

    @staticmethod
    def preprocess(data, transformer):
        return PreProcessTask.preprocess(
            data=data, transformer=transformer
        )
