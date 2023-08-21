import wx
import pandas as pd


def dfc_format_sequence(seq):
    output = []
    for item in seq:
        if isinstance(item, float):
            output.append("{0:.4g}".format(item))
        else:
            output.append(str(item))
    return output



class DataFrameControl(wx.ListCtrl):

    def __init__(self, parent, dataframe: pd.DataFrame, **kwargs):
        super().__init__(parent, style=wx.LC_REPORT | wx.BORDER_SUNKEN, **kwargs)
        self.set_data_frame(dataframe)

    def set_data_frame(self, dataframe: pd.DataFrame):
        self.ClearAll()
        for column_name in dataframe.columns:
            self.AppendColumn(column_name, width=90)
        for row in dataframe.itertuples(index=False):
            self.Append(dfc_format_sequence(row))
