import pandas
import scipy.stats
import wx
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from src.analyzers.abstractanalyzer import AbstractAnalyzer
from sklearn.decomposition import PCA

import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs
from src.markdownoutput import MarkdownOutput


class AgglomerativeClusteringAnalyzer(AbstractAnalyzer):

    @staticmethod
    def create_config_form(ctx: appctx.BPVAppContext):
        return [
            forminputs.OneOf(
                key="index_name",
                choices=ctx.get_selected_index_paths(),
            ),
            forminputs.OneOf(
                key="algorithm",
                choices=["ward", "average", "complete", "single"],
                default_choice_str="ward"
            ),
            forminputs.Number(
                key="num_of_classes",
                min_value=2,
                max_value=10,
                initial_value=3
            )
        ]

    def __init__(self, ctx: appctx.BPVAppContext, config: dict):
        self.app_context = ctx
        self.config = config
        self.pvalue = 0
        self.arr = 0
        self.h = 0

        pass

    def process(self, active_dataframe: pandas.DataFrame):
        # arr = active_dataframe[self.config["index_name"]]
        # self.pvalue = scipy.stats.shapiro(arr).pvalue
        self.arr = PCA(n_components=2).fit_transform(active_dataframe)  # transform data frame to 2D
        self.h = AgglomerativeClustering(linkage=self.config["algorithm"], n_clusters=self.config["num_of_classes"])
        self.h.fit(self.arr)

    def present(self):
        plt.title("COMPLETE (kolory odpowiadają wykrytym skupiskom)")
        plt.scatter(self.arr[:, 0], self.arr[:, 1], c=self.h.labels_)
        plt.show()

    def present_as_markdown(self, output: MarkdownOutput):
        pass


