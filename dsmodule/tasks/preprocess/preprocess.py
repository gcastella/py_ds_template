import logging
from sklearn.decomposition import PCA

from dsmodule.tasks import BaseTask

logger = logging.getLogger(__name__)


class PreProcessTask(BaseTask):
    def __init__(self):
        super(PreProcessTask, self).__init__("preprocess")

    def run(self):
        data = self.load(**self.input["extracted_data"])
        transformer = self.transformer(data)
        pp_data = self.preprocess(data, transformer)
        self.write(data=pp_data, **self.output["preprocessed_data"])
        self.write(data=transformer, **self.output["transformer"])

    @staticmethod
    def transformer(data):
        col_names = list(data.columns)
        variables = col_names[:-1]

        pca = PCA(1)
        pca.fit(data[variables])

        return pca

    @staticmethod
    def preprocess(data, transformer):
        col_names = list(data.columns)
        variables = col_names[:-1]

        df_pca = transformer.transform(data[variables])

        df_pp = data.copy()
        df_pp["pca_comp1"] = df_pca[:, 0]
        logger.info(f"Added first PCA component.")
        logger.debug(df_pp.head(5))

        return df_pp
