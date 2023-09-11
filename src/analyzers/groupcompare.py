import typing

import matplotlib.pyplot as plt
import pandas
import seaborn

import src.bpvappcontext as appctx
import src.gui.forminputs as forminputs
from src.analyzers.abstractanalyzer import AbstractAnalyzer
import src.registry as reg
import src.dataflow as dataflow


class GroupCompareAnalyzer(AbstractAnalyzer):
    def __init__(self, ctx: appctx.BPVAppContext, config: dict):
        self.ctx = ctx
        self.config = config
        self.final_df = None

    @staticmethod
    def create_config_form(ctx: appctx.BPVAppContext):
        applicable_indices = [
            idx.name for idx in reg.arr_patient_indices_registry
            if idx.applicable_to == "tag:num_series"
        ]
        return [
            forminputs.Text(
                key="group_a_name",
                initial_value="Group A"
            ),
            forminputs.SubsetOf(
                key="group_a_filters",
                choices=[entry.name for entry in reg.arr_session_filter_registry]
            ),
            forminputs.Text(
                key="group_b_name",
                initial_value="Group B"
            ),
            forminputs.SubsetOf(
                key="group_b_filters",
                choices=[entry.name for entry in reg.arr_session_filter_registry]
            ),
            forminputs.OneOf(
                key="collector_index",
                choices=applicable_indices,
                default_choice_str="mean"
            ),
            forminputs.OneOf(
                key="scale",
                choices=["log", "linear"],
                default_choice_str="linear"
            )
        ]

    def process(self, active_dataframe):
        group_names = [self.config["group_a_name"], self.config["group_b_name"]]
        group_dataframes: typing.List[pandas.DataFrame] = [
            dataflow.create_data_frame(
                self.ctx.get_txr_sessions(),
                self.config["group_a_filters"],
                self.ctx.get_selected_index_paths()
            ),
            dataflow.create_data_frame(
                self.ctx.get_txr_sessions(),
                self.config["group_b_filters"],
                self.ctx.get_selected_index_paths()
            )
        ]

        dfdata = []
        collector: reg.PatientIndex = reg.patient_indices_registry[self.config["collector_index"]]

        for grp_name, grp_df in zip(group_names, group_dataframes):
            df: pandas.DataFrame = grp_df
            for idx_name, idx_data in df.iteritems():
                metaidx = collector.calc_fn(idx_data)
                dfdata.append([idx_name, grp_name, metaidx])

        self.final_df = pandas.DataFrame(dfdata, columns=["Index", "Group", "Value"])

    def present(self):
        plt.figure(104)
        plt.clf()
        b_logy = self.config["scale"] == "log"
        self.final_df.pivot("Index", "Group", "Value").plot(kind='bar', ax=plt.gca(), logy=b_logy)
        plt.show()
