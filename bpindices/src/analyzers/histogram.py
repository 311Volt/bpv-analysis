import pandas

import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs
import src.dataflow.dataextractor as extractor

import matplotlib.pyplot as plt
import seaborn

class HistogramAnalyzer:

    @staticmethod
    def create_config_form(ctx: appctx.BPVAppContext):
        return [
            forminputs.OneOf(
                key="index_name",
                choices=ctx.get_selected_index_paths(),
            ),
            forminputs.Number(
                key="num_of_bins",
                min_value=2,
                max_value=1000,
                initial_value=20
            ),
            forminputs.Number(
                key="plt_fignum",
                min_value=2,
                max_value=500,
                initial_value=2
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
        self.dataframe: pandas.DataFrame = pandas.DataFrame()
        self.filters = []
        pass

    def process(self):
        self.filters = \
            self.app_context.get_selected_filters() if self.config["use_filters"] == "selected" else []

        self.dataframe = extractor.create_data_frame(
            self.app_context.txr_sessions,
            self.filters,
            [self.config["index_name"]]
        )

    def present(self):
        plt.figure(self.config["plt_fignum"])
        plt.clf()

        filters_title = "" if self.config["use_filters"] == "allow_all" else \
            "all that satisfy {}".format(self.filters)
        plt.title("Histogram for {} {}".format(
            self.config["index_name"],
            filters_title
        ))
        plt.hist(
            self.dataframe.to_numpy(),
            bins=self.config["num_of_bins"]
        )
        plt.show()
