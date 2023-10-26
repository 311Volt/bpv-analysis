import matplotlib.pyplot as plt
import pandas
import seaborn

import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs
from src.analyzers.abstractanalyzer import AbstractAnalyzer
from src.markdownoutput import MarkdownOutput
from sklearn.decomposition import PCA


class UMAPAnalyzer(AbstractAnalyzer):

    @staticmethod
    def create_config_form(ctx: appctx.BPVAppContext):
        return [
            forminputs.OneOf(
                key="metric",
                choices=["euclidean", "manhattan", "chebyshev", "minkowski", "canberra", "braycurtis", "haversine",
                         "mahalanobis", "wminkowski", "seuclidean", "cosine", "correlation"],
                default_choice_str="euclidean"
            ),
            forminputs.Number(
                key="neighbours",
                min_value=2,
                max_value=90,
                initial_value=15
            ),
            forminputs.Number(
                key="min_dist",
                min_value=0.0,
                max_value=1.0,
                initial_value=0.1
            )
        ]

    def __init__(self, ctx: appctx.BPVAppContext, config: dict):
        self.app_context = ctx
        self.config = config
        self.dataframe: pandas.DataFrame = pandas.DataFrame()
        self.filters = []
        self.columns = []
        pass

    def process(self, active_dataframe: pandas.DataFrame):
        from umap.umap_ import UMAP
        umap = UMAP(n_components=min(4, len(active_dataframe.columns)), metric=self.config["metric"], n_neighbors=self.config["neighbours"], min_dist=self.config["min_dist"])
        umap.fit(active_dataframe)
        self.columns = active_dataframe.columns
        self.dataframe = pandas.DataFrame(umap.embedding_, columns=self.columns)
        pass

    def plot(self):
        plt.figure(109)
        plt.clf()

        ax = seaborn.heatmap(self.dataframe, annot=True, cmap='coolwarm', center=0, fmt=".2f", linewidths=0.5)
        ax.figure.tight_layout()
        ax.figure.subplots_adjust(left=0.2, bottom=0.1, top=0.9, right=0.9)

        plt.title('PCA components for all test subjects')

    def present(self):
        self.plot()
        plt.show()

    def present_as_markdown(self, output: MarkdownOutput):

        output.write_paragraph(
            f"The following chart illustrates the directions of maximum variance in the data"
            f" for all patients subjected to this test."
        )

        self.plot()
        output.insert_current_pyplot_figure("pca")
