import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs
import src.dataflow.dataextractor as extractor
import scipy.stats

import wx

import matplotlib.pyplot as plt
import seaborn


class ShapiroAnalyzer:

    @staticmethod
    def create_config_form(ctx: appctx.BPVAppContext):
        return [
            forminputs.OneOf(
                key="index_name",
                choices=ctx.get_selected_index_paths(),
            )
        ]

    def __init__(self, ctx: appctx.BPVAppContext, config: dict):
        self.app_context = ctx
        self.config = config
        self.pvalue = 0
        pass

    def process(self):

        dataframe = extractor.create_data_frame(
            self.app_context.txr_sessions,
            self.app_context.get_selected_filters(),
            [self.config["index_name"]]
        )
        self.pvalue = scipy.stats.shapiro(dataframe.to_numpy()).pvalue

    def present(self):
        wx.MessageBox("p-value for {} is {}. This suggests that the data was drawn from a {} distribution.".format(
            self.config["index_name"],
            self.pvalue,
            "normal" if self.pvalue < 0.05 else "non-normal"
        ))
