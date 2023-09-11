import pandas
import wx

from src.gui.dataframe import DataFrameControl


class PreviewWindow(wx.Frame):
    def __init__(self, parent, df: pandas.DataFrame, **kwargs):
        super().__init__(parent, **kwargs)
        self.data_frame_list = DataFrameControl(self, df)
        self.vbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(self.data_frame_list)

        self.SetTitle("Extracted Data Live Preview")

    def set_dataframe(self, df: pandas.DataFrame):
        self.data_frame_list.set_data_frame(df)

    def export_to_csv(self, event):
        pass
