import configparser

import matplotlib.pyplot as plt
import pandas
import seaborn

import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs
from src.analyzers.abstractanalyzer import AbstractAnalyzer
from src.markdowndocument import MarkdownDocument
from sklearn.decomposition import PCA


class UMAPAnalyzer(AbstractAnalyzer):

    @staticmethod
    def create_config_form(ctx: appctx.BPVAppContext):
        config = configparser.RawConfigParser()
        config.read('src/analyzers/analyzers.cfg')
        details_dict = dict(config.items('umap'))

        return [
            forminputs.OneOf(
                key="metric",
                choices=["euclidean", "manhattan", "chebyshev", "minkowski", "canberra", "braycurtis", "haversine",
                         "mahalanobis", "wminkowski", "seuclidean", "cosine", "correlation"],
                default_choice_str=details_dict["metric"]
            ),
            forminputs.Number(
                key="neighbours",
                min_value=2,
                max_value=90,
                initial_value=int(details_dict["neighbours"])
            ),
            forminputs.Number( # dopisac
                key="min_dist * 10",
                min_value=0,
                max_value=10,
                initial_value=int(details_dict["min_dist * 10"])
            ),
            forminputs.Number(
                key="n_components",
                min_value=1,
                max_value=3,
                initial_value=int(details_dict["n_components"])
            )
        ]

    def __init__(self, ctx: appctx.BPVAppContext, config: dict):
        self.app_context = ctx
        self.config = config
        self.columns = []
        self.arr = 0
        self.n_components = self.config["n_components"]
        self.df = 0
        pass

    def process(self, active_dataframe: pandas.DataFrame):
        from umap.umap_ import UMAP
        self.n_components = min(self.n_components, len(active_dataframe.columns))
        umap = UMAP(n_components=self.n_components, metric=self.config["metric"], n_neighbors=self.config["neighbours"], min_dist=self.config["min_dist * 10"])
        self.arr = umap.fit_transform(active_dataframe)
        self.df = active_dataframe
        pass

    def plot(self):
        fig = plt.figure(109)
        plt.clf()

        if self.n_components == 1:
            ax = fig.add_subplot(111)
            ax.scatter(self.arr[:, 0], range(len(self.arr)))
        if self.n_components == 2:
            ax = fig.add_subplot(111)
            ax.scatter(self.arr[:, 0], self.arr[:, 1])
        if self.n_components == 3:
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(self.arr[:, 0], self.arr[:, 1], self.arr[:, 2], s=100)

        plt.title('UMAP components for all test subjects')

    def present_as_markdown(self, output: MarkdownDocument):

        output.write_paragraph(
            f"The following chart illustrates the directions of maximum variance in the data"
            f" for all patients subjected to this test."
        )

        self.plot()
        output.insert_current_pyplot_figure()
