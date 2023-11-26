import typing

import wx

from dataflow.dataextractor import create_data_frame
import datareader
from bpvappcontext import BPVAppContext
import src.gui.mainwindow as mainwindow


class ImplBPVAppContext(BPVAppContext):

    def __init__(self, file_resp_metadata: str, dir_resp_txr: str):
        self.txr_sessions = datareader.batch_import_txr_sessions(file_resp_metadata, dir_resp_txr)
        self.wxapp = wx.App()
        self.master_window = mainwindow.MainWindow(None, self, "BPV Analyzer")
        self.master_window.Show(True)
        self.slave_windows: typing.Dict[str, wx.Window] = dict()
        self.md_filename = "report"
        self.clear_report = True

    def run_app(self):
        self.wxapp.MainLoop()

    def exit(self):
        self.master_window.Destroy()
        for win in self.slave_windows.values():
            win.Destroy()

    def get_report_filename(self):
        return self.md_filename

    def set_report_filename(self, filename):
        self.md_filename = filename

    def set_clear_report(self, value: bool):
        self.clear_report = value

    def get_clear_report(self):
        return self.clear_report


    def get_selected_index_paths(self):
        return self.master_window.list_selected_index_paths()

    def get_selected_filters(self):
        return self.master_window.filter_checkboxes.get_selections()

    def create_active_dataframe(self):
        return create_data_frame(
            self.txr_sessions,
            self.get_selected_filters(),
            self.get_selected_index_paths()
        )

    def get_txr_sessions(self):
        return self.txr_sessions

    def get_master_window(self):
        return self.master_window

    def _on_slave_window_close(self, name):
        self.slave_windows[name].Destroy()
        self.slave_windows.pop(name)

    def slave_window_op(self, name, op):
        if name in self.slave_windows:
            op(self.slave_windows[name])

    def spawn_slave_window(self, name: str, window: wx.Window):
        if name in self.slave_windows:
            self.slave_windows[name].Destroy()
        self.slave_windows[name] = window
        self.slave_windows[name].Bind(wx.EVT_CLOSE, lambda _: self._on_slave_window_close(name))
        self.slave_windows[name].Show(True)

