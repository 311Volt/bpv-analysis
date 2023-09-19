import pandas
import scipy.stats
import wx
import matplotlib.pyplot as plt
import sklearn.cluster

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from src.analyzers import AbstractAnalyzer
import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs


class KMeansAnalyzer(AbstractAnalyzer):

    @staticmethod
    def create_config_form(ctx: appctx.BPVAppContext):
        return [
            forminputs.Number(
                key="num_classes",
                min_value=2,
                max_value=50,
                initial_value=3
            ),
            forminputs.OneOf(
                key="init_method",
                choices=["random", "k-means++"],
                default_choice_str="k-means++"
            ),
            forminputs.Number(
                key="max_iterations",
                min_value=2,
                max_value=2000,
                initial_value=300
            ),
            forminputs.OneOf(
                key="algorithm",
                choices=["lloyd", "elkan"],
                default_choice_str="lloyd"
            )
        ]

    def __init__(self, ctx: appctx.BPVAppContext, config: dict):
        self.app_context = ctx
        self.config = config
        self.arr2d = None
        self.kmeans = None

    def process(self, active_dataframe: pandas.DataFrame):
        self.kmeans = KMeans(
            n_clusters=self.config["num_classes"],
            init=self.config["init_method"],
            max_iter=self.config["max_iterations"],
            algorithm=self.config["algorithm"],
            n_init="auto"
        )

        self.arr2d = PCA(n_components=2).fit_transform(active_dataframe)
        self.kmeans.fit(active_dataframe)

        pass
        # arr = active_dataframe[self.config["index_name"]]
        # self.pvalue = scipy.stats.shapiro(arr).pvalue
        # self.arr = sklearn.decomposition.PCA(n_components=2).fit_transform(active_dataframe)  # transform data frame to 2D

        # self.h = AgglomerativeClustering(linkage=self.config["algorithm"], n_clusters=self.config["num_of_classes"])
        # self.h.fit(self.arr)

    def present(self):
        plt.figure(105)
        plt.clf()
        plt.title("K-Means clustering (visualized with 2D PCA)")
        plt.scatter(self.arr2d[:, 0], self.arr2d[:, 1], c=self.kmeans.labels_)
        plt.show()

    def present_as_markdown(self, output_filename: str):
        pass


