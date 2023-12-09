import configparser

import matplotlib.pyplot as plt
import pandas
import seaborn

import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs
from src.analyzers.abstractanalyzer import AbstractAnalyzer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from src.markdownoutput import MarkdownOutput

FIGNUM_CORRELATION = 1


class CorrelationAnalyzer(AbstractAnalyzer):

    @staticmethod
    def create_config_form(ctx: appctx.BPVAppContext):
        config = configparser.RawConfigParser()
        config.read('src/analyzers/analyzers.cfg')
        details_dict = dict(config.items('correlation'))

        return [
            forminputs.OneOf(
                key="mode",
                choices=["pearson", "spearman"],
                default_choice_str=details_dict["mode"]
            ),
            forminputs.Boolean(
                key="reduce_dimensions",
                initial_value=bool(details_dict["reduce_dimensions"])
            ),
            forminputs.OneOf(
                key="method_to_reduce_dimensions",
                choices=["UMAP", "t-SNE", "PCA"],
                default_choice_str=details_dict["method_to_reduce_dimensions"]
            ),
            forminputs.Number(
                key="number_of_dimensions",
                min_value=2,
                max_value=len(ctx.get_selected_index_paths()),
                initial_value=int(details_dict["number_of_dimensions"])
            )
        ]

    def __init__(self, ctx: appctx.BPVAppContext, config: dict):
        self.app_context = ctx
        self.config = config
        self.corr_mtx = None
        pass

    def process(self, active_dataframe: pandas.DataFrame):
        from umap.umap_ import UMAP
        arr = active_dataframe
        if self.config["reduce_dimensions"]:
            if self.config["method_to_reduce_dimensions"] == "UMAP":
                reducer = UMAP(n_components=self.config["number_of_dimensions"])
                arr = reducer.fit_transform(arr)
            elif self.config["method_to_reduce_dimensions"] == "t-SNE":
                arr = TSNE(n_components=self.config["number_of_dimensions"], perplexity=30).fit_transform(arr)
            else:
                arr = PCA(n_components=self.config["number_of_dimensions"]).fit_transform(
                    arr)  # transform data frame to 2D
            arr = pandas.DataFrame(data=arr, columns=[str(x) for x in range(self.config["number_of_dimensions"])])

        self.corr_mtx = arr.corr(method=self.config["mode"])

    def plot(self):
        plt.figure(FIGNUM_CORRELATION)
        plt.clf()
        ax = seaborn.heatmap(self.corr_mtx, annot=True, cmap='coolwarm', center=0, fmt=".2f", linewidths=0.5)
        ax.figure.tight_layout()
        ax.figure.subplots_adjust(left=0.2, bottom=0.1, top=0.9, right=0.9)
        plt.title("Correlation Matrix of selected parameters (mode={})".format(self.config["mode"]))

    def present(self):
        self.plot()
        plt.show()

    def create_markdown(self):
        if self.config["reduce_dimensions"]:
            parameters = "method to reduce number of dimensions: " + self.config["method_to_reduce_dimensions"] \
                         + ", number of classes: " + self.config["num_of_classes"] \
                         + ", linkage algorithm: " + self.config["algorithm"]
        return "We analysed data using agglomerative clustering. In the process following parameters were used:" \
               + parameters + " The results of our analysis are presented on the " \
                              "charts below."

    def present_as_markdown(self, output: MarkdownOutput):
        parameters = ["mode: " + self.config["mode"]]
        if self.config["reduce_dimensions"]:
            parameters.append("method to reduce dimensions: " + self.config["method_to_reduce_dimensions"])
            parameters.append("number of dimensions: " + str(self.config["number_of_dimensions"]))
        output.write_paragraph("Analysis using correlation with following parameters was conducted:")
        output.write_bullet_points(parameters)
        output.write_paragraph("Results can be seen on the chart below:")

        self.plot()
        output.insert_current_pyplot_figure("corr-vis2", "Correlation Visualization")


