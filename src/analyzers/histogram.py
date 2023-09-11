import matplotlib.pyplot as plt
import pandas

import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs
from src.analyzers.abstractanalyzer import AbstractAnalyzer


class HistogramAnalyzer(AbstractAnalyzer):

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
            )
        ]

    def __init__(self, ctx: appctx.BPVAppContext, config: dict):
        self.app_context = ctx
        self.config = config
        self.dataframe: pandas.DataFrame = pandas.DataFrame()
        self.filters = []
        pass

    def process(self, active_dataframe: pandas.DataFrame):
        self.dataframe = active_dataframe[self.config["index_name"]]
        self.filters = self.app_context.get_selected_filters()

    def present(self):
        plt.figure(self.config["plt_fignum"])
        plt.clf()

        filters_title = "" if len(self.filters) == 0 else \
            "(all that satisfy {})".format(self.filters)
        plt.title("Histogram for {} {}".format(
            self.config["index_name"],
            filters_title
        ))
        plt.hist(
            self.dataframe.to_numpy(),
            bins=self.config["num_of_bins"]
        )
        plt.show()
