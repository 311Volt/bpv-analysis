import configparser

import matplotlib.pyplot as plt
import pandas
import seaborn

import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs
from src.analyzers.abstractanalyzer import AbstractAnalyzer
from src.markdowndocument import MarkdownDocument
from sklearn.decomposition import PCA


class PCAAnalyzer(AbstractAnalyzer):

    @staticmethod
    def create_config_form(ctx: appctx.BPVAppContext):
        config = configparser.RawConfigParser()
        config.read('src/analyzers/analyzers.cfg')
        details_dict = dict(config.items('pca'))

        return [
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
        self.dataframe: pandas.DataFrame = pandas.DataFrame()
        self.filters = []
        self.columns = []
        self.n_components = self.config["n_components"]
        self.arr = 0
        pass

    def process(self, active_dataframe: pandas.DataFrame):
        self.n_components = min(self.n_components, len(active_dataframe.columns))
        pca = PCA(n_components=self.n_components)
        self.arr = pca.fit_transform(active_dataframe)
        self.columns = active_dataframe.columns
        self.dataframe = pandas.DataFrame(pca.components_, columns=self.columns)

    def plotTable(self):
        plt.figure(109)
        plt.clf()

        ax = seaborn.heatmap(self.dataframe, annot=True, cmap='coolwarm', center=0, fmt=".2f", linewidths=0.5)
        ax.figure.tight_layout()
        ax.figure.subplots_adjust(left=0.2, bottom=0.1, top=0.9, right=0.9)

        plt.title('PCA components for all test subjects')

    def plotChart(self):
        fig = plt.figure(110)
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

        plt.title('PCA components for all test subjects')

    def present(self):
        self.plotTable()
        plt.show()

        self.plotChart()
        plt.show()

    def present_as_markdown(self, output: MarkdownDocument):

        output.write_paragraph(
            f"The following chart illustrates the directions of maximum variance in the data"
            f" for all patients subjected to this test."
        )

        self.plotTable()
        output.insert_current_pyplot_figure("pca1")
        self.plotChart()
        output.insert_current_pyplot_figure("pca2")
