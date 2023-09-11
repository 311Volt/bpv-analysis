import dataclasses
import typing
import webbrowser

import wx
import wx.lib.agw.customtreectrl as wxtree

import src.bpvappcontext as appctx
import src.dataflow.dataextractor as extractor
import src.dataflow.indexpath as idxpath
import src.gui.analyzerlauncher as anl
import src.gui.regchecklistbox as regchk
import src.gui.treechecklistbox as treechk
import src.registry as reg
from src.gui.previewwindow import PreviewWindow

FIGNUM_CORRELATION = 1


@dataclasses.dataclass
class MainWindowConfig:
    selected_index_paths: typing.List[str]
    selected_filter_names: typing.List[str]


class MainWindow(wx.Frame):

    def __init__(self, parent, ctx: appctx.BPVAppContext, title):
        wx.Frame.__init__(self, parent, title=title, size=(640, 480))
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

        self.filter_checkboxes = regchk.RegCheckListBox(self, self.filter_choices, pos=(393, 33), size=(157, 197))

        self.path_checkboxes = treechk.TreeCheckListBox(self, pos=(33, 33), size=(317, 197))

        for extractorentry in self.extractor_choices:
            self.path_checkboxes.add_item_group(extractorentry, self.create_path_checkbox_items(extractorentry))

        self.filter_checkboxes.set_selections(["age_valid"])
        self.path_checkboxes.set_selections(["bp_sys/mean", "bp_sys/stddev", "metadata/age"])

        self.open_preview_btn = wx.Button(self, -1, "Data View...", pos=(30, 265), size=(160, 24))
        self.gen_markdown_btn = wx.Button(self, -1, "MD Report Generator...", pos=(30, 295), size=(160, 24))
        self.analyze_btn = wx.Button(self, -1, "Analyze...", pos=(385, 265), size=(160, 24))

        self.gen_markdown_btn.Disable()

        self.Bind(wx.EVT_BUTTON, self.show_preview, self.open_preview_btn)
        self.Bind(wx.EVT_BUTTON, self.generate_markdown, self.gen_markdown_btn)
        self.Bind(wx.EVT_BUTTON, self.show_analyzer_launcher, self.analyze_btn)

        self.Bind(wx.EVT_CHECKLISTBOX, self.update_preview)
        self.Bind(wxtree.EVT_TREE_ITEM_CHECKED, self.update_preview)
        self.Bind(wx.EVT_COMBOBOX, self.update_preview)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.app_context = ctx

    @staticmethod
    def create_path_checkbox_items(extractor_entry: regchk.CheckListEntry):
        items = []
        for index in reg.arr_patient_indices_registry:
            if idxpath.index_applies_to_extractor(index.name, extractor_entry.name):
                items.append(regchk.CheckListEntry(
                    name=idxpath.create_combination_path(extractor_entry.name, index.name),
                    display_name=index.display_name
                ))
        return items

    def get_config(self) -> MainWindowConfig:
        return MainWindowConfig(
            selected_index_paths=self.list_selected_index_paths(),
            selected_filter_names=self.filter_checkboxes.get_selections()
        )

    def update_preview(self, event):
        self.app_context.slave_window_op(
            "data_preview",
            lambda preview_window: preview_window.set_dataframe(self.create_data_frame())
        )
        self.app_context.slave_window_op(
            "analyzer_launcher",
            lambda analyzer_window: analyzer_window.update()
        )

    def list_selected_index_paths(self):
        return self.path_checkboxes.get_selections()

    def show_analyzer_launcher(self, event):
        launcher = anl.AnalyzerLauncher(None, self.app_context, size=(480, 360))
        self.app_context.spawn_slave_window("analyzer_launcher", launcher)

    def create_data_frame(self):
        return extractor.create_data_frame(
            sessions=self.app_context.txr_sessions,
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
        pwin = PreviewWindow(None, df)
        self.app_context.spawn_slave_window("data_preview", pwin)

    def generate_markdown(self, event):
        pass

    def on_close(self, event):
        self.app_context.exit()
