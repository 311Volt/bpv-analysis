import seaborn
import wx

import src.registry as reg
import src.dataflow.indexpath as idxpath
import src.datareader as datareader
import src.dataflow.dataextractor as extractor
import src.gui.regchecklistbox as regchk
import src.gui.treechecklistbox as treechk
import wx.lib.agw.customtreectrl as wxtree
from src.gui.previewwindow import PreviewWindow

import matplotlib.pyplot as plt

import webbrowser

FIGNUM_CORRELATION = 1


class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(640, 360))
        self.SetBackgroundColour(wx.NullColour)
        self.SetMinSize(self.GetSize())

        self.index_choices = [
            regchk.CheckListEntry(name=idx.name, display_name=idx.display_name)
            for idx in reg.arr_patient_indices_registry
        ]
        self.filter_choices = [
            regchk.CheckListEntry(name=idx.name, display_name=idx.display_name)
            for idx in reg.arr_session_filter_registry
        ]
        self.extractor_choices = [
            regchk.CheckListEntry(name=idx.name, display_name=idx.display_name)
            for idx in reg.arr_series_extractor_registry
        ]

        self.group_box_1 = wx.StaticBox(self, label="Columns", pos=(25, 15), size=(330, 220))
        self.group_box_2 = wx.StaticBox(self, label="Filters", pos=(385, 15), size=(170, 220))

        self.filter_checkboxes = regchk.RegCheckListBox(self, self.filter_choices, pos=(390, 30), size=(160, 200))

        self.path_checkboxes = treechk.TreeCheckListBox(self, pos=(30, 30), size=(320, 200))
        for extractorentry in self.extractor_choices:
            self.path_checkboxes.add_item_group(extractorentry, self.create_path_checkbox_items(extractorentry))

        self.filter_checkboxes.set_selections(["age_valid"])
        self.path_checkboxes.set_selections(["bp_sys/mean", "bp_sys/stddev", "metadata/age"])

        self.open_preview_btn = wx.Button(self, -1, "Data View...", pos=(30, 265), size=(160, 24))
        self.gen_markdown_btn = wx.Button(self, -1, "MD Report Generator...", pos=(30, 295), size=(160, 24))
        self.corr_mtx_btn = wx.Button(self, -1, "Correlation Matrix View...", pos=(205, 265), size=(160, 24))
        self.stat_view_btn = wx.Button(self, -1, "Statistics View...", pos=(385, 265), size=(160, 24))

        self.corr_mode_sel_label = wx.StaticText(self, pos=(205, 300), size=(50, 24), style=wx.ALIGN_RIGHT)
        self.corr_mode_sel_label.SetLabel("Mode: ")
        self.corr_mode_sel = wx.ComboBox(
            self,
            name="Correlation Mode",
            choices=["Pearson", "Spearman"], value="Pearson",
            style=wx.CB_DROPDOWN | wx.CB_READONLY,
            pos=(255, 295), size=(110, 24)
        )
        self.gen_markdown_btn.Disable()

        self.preview_window = None

        self.Bind(wx.EVT_BUTTON, self.show_preview, self.open_preview_btn)
        self.Bind(wx.EVT_BUTTON, self.generate_markdown, self.gen_markdown_btn)
        self.Bind(wx.EVT_BUTTON, self.show_corr_matrix, self.corr_mtx_btn)

        self.Bind(wx.EVT_CHECKLISTBOX, self.update_preview)
        self.Bind(wxtree.EVT_TREE_ITEM_CHECKED, self.update_preview)
        self.Bind(wx.EVT_COMBOBOX, self.update_preview)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.txr_sessions = datareader.batch_import_txr_sessions("RESP_metadata.csv")

    def create_path_checkbox_items(self, extractor_entry: regchk.CheckListEntry):
        items = []
        for index in reg.arr_patient_indices_registry:
            if idxpath.index_applies_to_extractor(index.name, extractor_entry.name):
                items.append(regchk.CheckListEntry(
                    name=idxpath.create_combination_path(extractor_entry.name, index.name),
                    display_name=index.display_name
                ))
        return items

    def update_preview(self, event):
        if self.preview_window is not None:
            self.preview_window.set_dataframe(self.create_data_frame())
        if plt.fignum_exists(FIGNUM_CORRELATION):
            self.show_corr_matrix(None)

    def list_selected_index_paths(self):
        return self.path_checkboxes.get_selections()

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

    def get_correlation_mode(self):
        return self.corr_mode_sel.GetStringSelection().lower()

    def show_preview(self, event):
        df = self.create_data_frame()
        self.preview_window = PreviewWindow(None, df, on_close_callback=self.acknowledge_preview_close)

    def acknowledge_preview_close(self):
        self.preview_window = None

    def show_corr_matrix(self, event):
        corr_mtx = self.create_data_frame().corr(method=self.get_correlation_mode())
        fig = plt.figure(FIGNUM_CORRELATION)
        plt.clf()
        ax = seaborn.heatmap(corr_mtx, annot=True, cmap='coolwarm', center=0, fmt=".2f", linewidths=0.5)
        ax.figure.tight_layout()
        ax.figure.subplots_adjust(left=0.2, bottom=0.1, top=0.9, right=0.9)
        plt.title("Correlation Matrix of selected parameters (mode={})".format(self.get_correlation_mode()))
        plt.show()

    def generate_markdown(self, event):
        pass

    def on_close(self, event):
        if self.preview_window is not None:
            self.preview_window.Close()
        self.Destroy()
