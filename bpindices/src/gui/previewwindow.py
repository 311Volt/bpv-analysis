import typing

import pandas
import wx
from src.gui.dataframe import DataFrameControl
from src.gui.subwindow import SubWindow


class PreviewWindow(SubWindow):
    def __init__(self, parent, df: pandas.DataFrame, **kwargs):
        super().__init__(parent, **kwargs)
        self.data_frame_list = DataFrameControl(self, df)
        self.vbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(self.data_frame_list)

        self.SetTitle("Extracted Data Live Preview")
        self.Show(True)

    def set_dataframe(self, df: pandas.DataFrame):
        self.data_frame_list.set_data_frame(df)

    def export_to_csv(self, event):
        pass
