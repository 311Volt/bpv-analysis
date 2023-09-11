import matplotlib.pyplot as plt
import pandas
import seaborn

import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs

FIGNUM_CORRELATION = 1


class CorrelationAnalyzer:

    @staticmethod
    def create_config_form(ctx: appctx.BPVAppContext):
        return [
            forminputs.OneOf(
                key="mode",
                choices=["pearson", "spearman"],
                default_choice_str="pearson"
            )
        ]

    def __init__(self, ctx: appctx.BPVAppContext, config: dict):
        self.app_context = ctx
        self.config = config
        self.corr_mtx = None
        pass

    def process(self, active_dataframe: pandas.DataFrame):
        self.corr_mtx = active_dataframe.corr(method=self.config["mode"])

    def present(self):
        plt.figure(FIGNUM_CORRELATION)
        plt.clf()
        ax = seaborn.heatmap(self.corr_mtx, annot=True, cmap='coolwarm', center=0, fmt=".2f", linewidths=0.5)
        ax.figure.tight_layout()
        ax.figure.subplots_adjust(left=0.2, bottom=0.1, top=0.9, right=0.9)
        plt.title("Correlation Matrix of selected parameters (mode={})".format(self.config["mode"]))
        plt.show()
