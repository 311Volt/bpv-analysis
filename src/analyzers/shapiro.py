import pandas
import scipy.stats
import wx

import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs
import src.registry as reg

from src.analyzers.abstractanalyzer import AbstractAnalyzer
from src.markdownoutput import MarkdownOutput


class ShapiroAnalyzer(AbstractAnalyzer):

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

    def process(self, active_dataframe: pandas.DataFrame):
        arr = active_dataframe[self.config["index_name"]]
        self.pvalue = scipy.stats.shapiro(arr).pvalue

    def conclusion_str(self):
        return "This suggests that the data was drawn from a {} distribution.".format(
            "normal" if self.pvalue < 0.05 else "non-normal"
        )

    def present(self):
        wx.MessageBox("p-value for {} is {}. {}".format(
            self.config["index_name"],
            self.pvalue,
            self.conclusion_str()
        ))

    def present_as_markdown(self, output: MarkdownOutput):
        output.write_paragraph(
            f"The value of the index {self.config['index_name']} has been subjected to the "
            f"Shapiro-Wilk test, which yielded a p-value of **{self.pvalue}**. "
            f"{self.conclusion_str()}"
        )
