import matplotlib.pyplot as plt
import pandas
import seaborn

import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs
from src.analyzers.abstractanalyzer import AbstractAnalyzer
from src.markdownoutput import MarkdownOutput
from sklearn.decomposition import PCA


class PCAAnalyzer(AbstractAnalyzer):

    @staticmethod
    def create_config_form(ctx: appctx.BPVAppContext):
        return [
        ]

    def __init__(self, ctx: appctx.BPVAppContext, config: dict):
        self.app_context = ctx
        self.config = config
        self.dataframe: pandas.DataFrame = pandas.DataFrame()
        self.filters = []
        self.columns = []
        pass

    def process(self, active_dataframe: pandas.DataFrame):
        pca = PCA(n_components=max(4, len(self.columns)))
        pca.fit(active_dataframe)
        self.columns = active_dataframe.columns
        self.dataframe = pandas.DataFrame(pca.components_, columns=self.columns)

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
