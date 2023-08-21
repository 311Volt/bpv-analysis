import wx

import src.registry as reg
import src.dataflow.indexpath as idxpath
import src.datareader as datareader
import src.dataflow.dataextractor as extractor
import src.gui.regchecklistbox as regchk
from src.gui.previewwindow import PreviewWindow

import webbrowser


class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(640, 360))
        self.SetBackgroundColour(wx.NullColour)
        self.SetMinSize(self.GetSize())

        index_choices = [
            regchk.CheckListEntry(name=idx.name, display_name=idx.display_name)
            for idx in reg.arr_patient_indices_registry
        ]
        filter_choices = [
            regchk.CheckListEntry(name=idx.name, display_name=idx.display_name)
            for idx in reg.arr_session_filter_registry
        ]
        extractor_choices = [
            regchk.CheckListEntry(name=idx.name, display_name=idx.display_name)
            for idx in reg.arr_series_extractor_registry
        ]

        self.group_box_1 = wx.StaticBox(self, label="Indices", pos=(25, 15), size=(170, 220))
        self.group_box_2 = wx.StaticBox(self, label="Filters", pos=(205, 15), size=(170, 220))
        self.group_box_3 = wx.StaticBox(self, label="Extractors", pos=(385, 15), size=(170, 220))

        self.index_checkboxes = regchk.RegCheckListBox(self, index_choices, pos=(30, 30), size=(160, 200))
        self.filter_checkboxes = regchk.RegCheckListBox(self, filter_choices, pos=(210, 30), size=(160, 200))
        self.extractor_checkboxes = regchk.RegCheckListBox(self, extractor_choices, pos=(390, 30), size=(160, 200))

        self.filter_checkboxes.set_selections(["age_valid"])
        self.index_checkboxes.set_selections(["age", "mean", "stddev", "arv"])
        self.extractor_checkboxes.set_selections(["bp_systolic", "metadata"])

        self.open_preview_btn = wx.Button(self, -1, "Open Preview", pos=(30, 265), size=(160, 24))
        self.gen_markdown_btn = wx.Button(self, -1, "Generate Markdown", pos=(30, 295), size=(160, 24))
        self.gen_markdown_btn.Disable()

        self.preview_window = None

        self.Bind(wx.EVT_BUTTON, self.show_preview, self.open_preview_btn)
        self.Bind(wx.EVT_BUTTON, self.generate_markdown, self.gen_markdown_btn)
        self.Bind(wx.EVT_CHECKLISTBOX, self.update_preview)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.txr_sessions = datareader.batch_import_txr_sessions("RESP_metadata.csv")

    def update_preview(self, event):
        if self.preview_window is not None:
            self.preview_window.set_dataframe(self.create_data_frame())

    def list_selected_index_paths(self):
        return idxpath.create_combination_paths(
            self.extractor_checkboxes.get_selections(),
            self.index_checkboxes.get_selections()
        )

    def create_data_frame(self):
        return extractor.create_data_frame(
            sessions=self.txr_sessions,
            filter_names=self.filter_checkboxes.get_selections(),
            index_paths=self.list_selected_index_paths()
        )

    def show_preview_html(self, event):
        df = self.create_data_frame()
        with open("bpframe.html", "w") as htmlfile:
            htmlfile.write(df.to_html())
            webbrowser.open("bpframe.html")
        pass

    def show_preview(self, event):
        df = self.create_data_frame()
        self.preview_window = PreviewWindow(None, df)
        self.preview_window.Show(True)
        self.preview_window.SetTitle("Extracted Data Live Preview")
        self.preview_window.on_close_callback = self.acknowledge_window_close

    def acknowledge_window_close(self):
        self.preview_window = None

    def generate_markdown(self, event):
        pass

    def on_close(self, event):
        if self.preview_window is not None:
            self.preview_window.Close()
        self.Destroy()
