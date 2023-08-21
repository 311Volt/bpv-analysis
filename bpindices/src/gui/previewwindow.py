import typing

import pandas
import wx
from src.gui.dataframe import DataFrameControl


class PreviewWindow(wx.Frame):
    def __init__(self, parent, df: pandas.DataFrame, **kwargs):
        super().__init__(parent, **kwargs)
        self.data_frame_list = DataFrameControl(self, df)
        self.on_close_callback = None
        self.vbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(self.data_frame_list, border=15)

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def set_dataframe(self, df: pandas.DataFrame):
        self.data_frame_list.set_data_frame(df)

    def on_close(self, event):
        self.on_close_callback()
        self.Destroy()
