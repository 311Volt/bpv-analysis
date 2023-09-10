import typing

import datareader
import gui
import wx


class BPVAppContext:

    def __init__(self, file_resp_metadata: str, dir_resp_txr: str):
        self.txr_sessions = datareader.batch_import_txr_sessions(file_resp_metadata, dir_resp_txr)
        self.wxapp = wx.App()
        self.master_window = gui.MainWindow(None, self, "BPV Analyzer")
        self.master_window.Show(True)
        self.slave_windows: typing.Dict[str, wx.Window] = dict()

    def run_app(self):
        self.wxapp.MainLoop()

    def exit(self):
        self.master_window.Destroy()
        for win in self.slave_windows.values():
            win.Destroy()

    def get_selected_index_paths(self):
        return self.master_window.list_selected_index_paths()

    def get_selected_filters(self):
        return self.master_window.filter_checkboxes.get_selections()

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

