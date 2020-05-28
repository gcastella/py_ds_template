import logging
from sklearn.decomposition import PCA

from python_package.tasks import BaseTask

logger = logging.getLogger(__name__)


class PreProcessTask(BaseTask):
    def __init__(self):
        super(PreProcessTask, self).__init__("preprocess")

    def run(self):
        data = self.load(file=self.input)
        pp_data = self.preprocess(data)
        self.write(data=pp_data, file=self.output)

    def preprocess(self, data):
        col_names = list(data.columns)
        variables = col_names[:-1]

        pca = PCA(1)
        df_pca = pca.fit_transform(data[variables])

        df_pp = data.copy()
        df_pp["pca_comp1"] = df_pca[:, 0]
        logger.info(f"Added first PCA component.")
        logger.debug(df_pp.head(5))

        return df_pp
