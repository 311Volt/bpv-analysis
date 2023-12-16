import pandas
import scipy.stats
import wx
import configparser
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from src.analyzers.abstractanalyzer import AbstractAnalyzer
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs
from src.markdowndocument import MarkdownDocument
import os

class AgglomerativeClusteringAnalyzer(AbstractAnalyzer):

    @staticmethod
    def create_config_form(ctx: appctx.BPVAppContext):
        config = configparser.RawConfigParser()
        config.read('src/analyzers/analyzers.cfg')
        details_dict = dict(config.items('agglomerativec'))

        return [
            forminputs.OneOf(
                key="algorithm",
                choices=["ward", "average", "complete", "single"],
                default_choice_str=details_dict["algorithm"]
            ),
            forminputs.OneOf(
                key="method_to_reduce_dimensions",
                choices=["UMAP", "t-SNE", "PCA"],
                default_choice_str=details_dict["method_to_reduce_dimensions"]
            ),
            forminputs.Number(
                key="num_of_classes",
                min_value=2,
                max_value=10,
                initial_value=int(details_dict["num_of_classes"])
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
        from umap.umap_ import UMAP
        if self.config["method_to_reduce_dimensions"] == "UMAP":
            reducer = UMAP(n_components=2)
            self.arr = reducer.fit_transform(active_dataframe)
        elif self.config["method_to_reduce_dimensions"] == "t-SNE":
            self.arr = TSNE(n_components=2, perplexity=30).fit_transform(active_dataframe)
        else:
            self.arr = PCA(n_components=2).fit_transform(active_dataframe)
        self.h = AgglomerativeClustering(linkage=self.config["algorithm"], n_clusters=self.config["num_of_classes"])
        self.h.fit(self.arr)

    def plot_chart(self):
        plt.title("Hierarchical Grouping")
        plt.scatter(self.arr[:, 0], self.arr[:, 1], c=self.h.labels_)

    def plot_dendrogram(self):
        dendrogram_plot = dendrogram(linkage(self.h.children_, method=self.h.linkage))
        plt.title('Dendrogram')
        plt.ylabel('Distance')

    def present(self):
        self.plot_chart()
        plt.show()

        self.plot_dendrogram()
        plt.show()

    def present_as_markdown(self, output: MarkdownDocument):
        parameters = ["linkage algorithm: " + self.config["algorithm"],
                      "method to reduce dimensions: " + self.config["method_to_reduce_dimensions"],
                      "number of classes: " + str(self.config["num_of_classes"])]
        output.write_paragraph("Analysis using agglomerative clustering with following parameters was conducted:")
        output.write_bullet_points(parameters)
        output.write_paragraph("Results can be seen on the charts below:")

        self.plot_chart()
        output.insert_current_pyplot_figure("aggl-vis1", "Hierarchical Grouping Visualization")
        self.plot_dendrogram()
        output.insert_current_pyplot_figure("aggl-vis2", "Hierarchical Grouping Dendrogram Visualization")
