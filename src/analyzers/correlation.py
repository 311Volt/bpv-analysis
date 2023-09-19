import matplotlib.pyplot as plt
import pandas
import seaborn

import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs
from src.analyzers.abstractanalyzer import AbstractAnalyzer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap
from src.markdownoutput import MarkdownOutput

FIGNUM_CORRELATION = 1


class CorrelationAnalyzer(AbstractAnalyzer):

    @staticmethod
    def create_config_form(ctx: appctx.BPVAppContext):
        return [
            forminputs.OneOf(
                key="mode",
                choices=["pearson", "spearman"],
                default_choice_str="pearson"
            ),
            forminputs.Text(
                key="file_name",
                initial_value="correlation"
            ),
            forminputs.Boolean(
                key="reduce_dimensions",
                initial_value=False
            ),
            forminputs.OneOf(
                key="method_to_reduce_dimensions",
                choices=["UMAP", "t-SNE", "PCA"],
                default_choice_str="PCA"
            ),
            forminputs.Number(
                key="number_of_dimensions",
                min_value=2,
                max_value=len(ctx.get_selected_index_paths()),
                initial_value=2
            )
        ]

    def __init__(self, ctx: appctx.BPVAppContext, config: dict):
        self.app_context = ctx
        self.config = config
        self.corr_mtx = None
        pass

    def process(self, active_dataframe: pandas.DataFrame):
        arr = active_dataframe
        if self.config["reduce_dimensions"]:
            if self.config["method_to_reduce_dimensions"] == "UMAP":
                reducer = umap.UMAP(n_components=self.config["number_of_dimensions"])
                arr = reducer.fit_transform(arr)
            elif self.config["method_to_reduce_dimensions"] == "t-SNE":
                arr = TSNE(n_components=self.config["number_of_dimensions"], perplexity=30).fit_transform(arr)
            else:
                arr = PCA(n_components=self.config["number_of_dimensions"]).fit_transform(
                    arr)  # transform data frame to 2D
            arr = pandas.DataFrame(data=arr, columns=[str(x) for x in range(self.config["number_of_dimensions"])])

        self.corr_mtx = arr.corr(method=self.config["mode"])

    def present(self):
        plt.figure(FIGNUM_CORRELATION)
        plt.clf()
        ax = seaborn.heatmap(self.corr_mtx, annot=True, cmap='coolwarm', center=0, fmt=".2f", linewidths=0.5)
        ax.figure.tight_layout()
        ax.figure.subplots_adjust(left=0.2, bottom=0.1, top=0.9, right=0.9)
        plt.title("Correlation Matrix of selected parameters (mode={})".format(self.config["mode"]))
        plt.show()

    def present_as_markdown(self, output: MarkdownOutput):
        pass


