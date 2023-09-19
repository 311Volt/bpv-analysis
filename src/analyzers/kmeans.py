import pandas
import pandas as pd
import scipy.stats
import wx
import matplotlib.pyplot as plt
import sklearn.cluster
import numpy as np

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from src.gui.previewwindow import PreviewWindow

import src.registry as reg
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
        self.result = None

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

        clusters = [
            active_dataframe[self.kmeans.labels_[active_dataframe.index] == i]
            for i in range(self.kmeans.n_clusters)
        ]

        # print(clusters)

        results_dict = dict()
        for idxname in active_dataframe.columns:
            out_col = []
            for clusteridx in range(len(clusters)):
                mc = reg.patient_indices_registry["mean"]
                sc = reg.patient_indices_registry["stddev"]
                mean = mc.calc_fn((clusters[clusteridx][idxname].to_numpy(),))
                std = sc.calc_fn((clusters[clusteridx][idxname].to_numpy(),))
                out_col.append("{0:.4g} +/- {1:.4g}".format(mean, std))
            results_dict["{}_stat".format(idxname)] = out_col

        self.result = pandas.DataFrame(
            data=results_dict,
            index=["cluster{}".format(i) for i in range(len(clusters))]
        )

        # print(self.result)

    def present(self):
        plt.figure(105)
        plt.clf()
        plt.title("K-Means clustering (visualized with 2D PCA)")
        plt.scatter(self.arr2d[:, 0], self.arr2d[:, 1], c=self.kmeans.labels_)
        plt.show()

        self.app_context.spawn_slave_window(
            "kmeans_present",
            PreviewWindow(None, self.result)
        )
        self.app_context.slave_window_op("kmeans_present", lambda win: win.SetTitle("K-Means Cluster Stats"))

    def present_as_markdown(self, output_filename: str):
        pass


