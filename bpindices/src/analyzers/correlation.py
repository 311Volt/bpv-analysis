import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs
import src.dataflow.dataextractor as extractor

import matplotlib.pyplot as plt
import seaborn

FIGNUM_CORRELATION = 1


class CorrelationAnalyzer:

    @staticmethod
    def create_config_form(ctx: appctx.BPVAppContext):
        return [
            forminputs.OneOf(
                key="mode",
                choices=["pearson", "spearman"],
                default_choice_str="pearson"
            ),
            forminputs.SubsetOf(
                key="indices",
                choices=ctx.get_selected_index_paths(),
                select_all_by_default=True
            ),
            forminputs.OneOf(
                key="use_filters",
                choices=["selected", "allow_all"],
                default_choice_str="selected"
            )
        ]

    def __init__(self, ctx: appctx.BPVAppContext, config: dict):
        self.app_context = ctx
        self.config = config
        self.corr_mtx = None
        pass

    def process(self):
        filters = \
            self.app_context.get_selected_filters() if self.config["use_filters"] == "selected" else []

        dataframe = extractor.create_data_frame(
            self.app_context.txr_sessions,
            filters,
            self.config["indices"]
        )
        self.corr_mtx = dataframe.corr(method=self.config["mode"])

    def present(self):
        plt.figure(FIGNUM_CORRELATION)
        plt.clf()
        ax = seaborn.heatmap(self.corr_mtx, annot=True, cmap='coolwarm', center=0, fmt=".2f", linewidths=0.5)
        ax.figure.tight_layout()
        ax.figure.subplots_adjust(left=0.2, bottom=0.1, top=0.9, right=0.9)
        plt.title("Correlation Matrix of selected parameters (mode={})".format(self.config["mode"]))
        plt.show()
