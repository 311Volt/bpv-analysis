import configparser
import pickle
import typing

import wx

import src.gui.form as frm
import src.registry as reg
from src.analyzers import AbstractAnalyzer
from src.markdowndocument import MarkdownDocument
from src.bpvappcontext import BPVAppContext
import src.gui.filenameeditor as fne
import wx.lib.masked.numctrl
import gzip


class AnalyzerLauncher(wx.Frame):
    def __init__(self, parent, ctx: BPVAppContext, **kwargs):
        super().__init__(parent, **kwargs)

        self.vsizer = wx.BoxSizer(wx.VERTICAL)

        self.ctrlpanel = wx.Panel(self, style=wx.BORDER_SUNKEN)
        self.statuspanel = wx.Panel(self, style=wx.BORDER_SUNKEN)
        self.formpanel = wx.Panel(self)
        self.update_flag = True

        self.ctx = ctx

        self.label_analyzer_choice = wx.StaticText(
            self.ctrlpanel, label="Analyzer: ",
            pos=(10, 7)
        )
        self.analyzer_disp_names = [anal.display_name for anal in reg.arr_analyzer_registry]
        self.analyzer_names = [anal.name for anal in reg.arr_analyzer_registry]
        self.analyzer_choice = wx.ComboBox(
            self.ctrlpanel,
            name="Analyzer",
            choices=self.analyzer_disp_names,
            value=self.analyzer_disp_names[0],
            style=wx.CB_DROPDOWN | wx.CB_READONLY,
            pos=(70, 5)
        )
        self.add_to_report_btn = wx.Button(self.ctrlpanel, -1, "Add to report", pos=(220, 5))
        self.clear_report_btn = wx.Button(self.ctrlpanel, -1, "Clear report", pos=(320, 5))
        self.load_report_btn = wx.Button(self.ctrlpanel, -1, "Load...", pos=(400, 5), size=(50, 30))
        self.save_report_btn = wx.Button(self.ctrlpanel, -1, "Save...", pos=(450, 5), size=(50, 30))

        self.cur_indices_list_box = wx.ListBox(
            self.statuspanel, size=(220, 100),
            choices=ctx.get_selected_index_paths()
        )
        self.cur_filters_list_box = wx.ListBox(
            self.statuspanel, size=(220, 100),
            choices=ctx.get_selected_filters()
        )

        self.statussizer = wx.BoxSizer(wx.HORIZONTAL)
        self.statussz1 = wx.StaticBoxSizer(wx.VERTICAL, self.statuspanel, "Using indices: ")
        self.statussz1.Add(self.cur_indices_list_box, border=5)
        self.statussz2 = wx.StaticBoxSizer(wx.VERTICAL, self.statuspanel, "Using filters: ")
        self.statussz2.Add(self.cur_filters_list_box, border=5)

        self.statussizer.Add(self.statussz1, border=5)
        self.statussizer.Add(self.statussz2, border=5)
        self.statuspanel.SetSizer(self.statussizer)

        self.vsizer.Add(
            self.ctrlpanel, flag=wx.EXPAND | wx.ALL, border=5
        )
        self.vsizer.Add(
            self.statuspanel, flag=wx.EXPAND | wx.ALL, border=5
        )
        self.vsizer.Add(
            self.formpanel, flag=wx.EXPAND | wx.ALL, border=5
        )

        self.update()
        self.SetSizer(self.vsizer)
        self.Bind(wx.EVT_BUTTON, self.load_report, self.load_report_btn)
        self.Bind(wx.EVT_BUTTON, self.save_report, self.save_report_btn)
        self.Bind(wx.EVT_BUTTON, self.add_to_report, self.add_to_report_btn)
        self.Bind(wx.EVT_BUTTON, self.clear_md_report, self.clear_report_btn)
        self.Bind(wx.EVT_COMBOBOX, self.update_impl, self.analyzer_choice)

        # TODO find some way to generically handle all command events coming from the form because this is horrible
        # as of 2023-12-16 google and chatgpt are completely clueless
        wxEVT_ANY_FORM_CONTROL = [
            wx.wxEVT_CHECKBOX,
            wx.lib.masked.numctrl.wxEVT_COMMAND_MASKED_NUMBER_UPDATED,
            wx.wxEVT_COMBOBOX,
            wx.wxEVT_CHECKLISTBOX,
            wx.wxEVT_CHAR,
            wx.wxEVT_BUTTON
        ]

        self.Bind(wx.PyEventBinder(wxEVT_ANY_FORM_CONTROL, 1), self.on_form_update)

    def on_form_update(self, event: typing.Optional[wx.Event]):
        # TODO run this asynchronously in the background
        # might be problematic because matplotlib does not like running outside the main thread

        if event is not None:
            event.Skip()
        if self.update_flag:
            self.ctx.set_current_analysis_preview(self.run_analyzer())
            self.ctx.get_server().trigger_update()

    def save_report(self, event):
        with wx.FileDialog(self, "Save report", wildcard="BPV Analyzer Reports (*.bpr)|*.bpr",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, defaultFile="report.bpr") as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            try:
                with gzip.open(pathname, 'wb') as file:
                    pickle.dump(self.ctx.get_current_report(), file)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)
        pass

    def load_report(self, event):
        with wx.FileDialog(self, "Open report", wildcard="BPV Analyzer Reports (*.bpr)|*.bpr",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            try:
                with gzip.open(pathname, 'rb') as file:
                    self.ctx.set_current_report(pickle.load(file))
                    self.ctx.get_server().trigger_update()
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)

    def get_current_analyzer_desc(self):
        return reg.arr_analyzer_registry[self.analyzer_choice.GetSelection()]

    def get_current_config_for_analyzer(self):
        return self.formpanel.collect()

    def update_impl(self, event):
        self.update_flag = False
        analyzer_desc = self.get_current_analyzer_desc()
        analyzer_name = analyzer_desc.name

        self.vsizer.Detach(self.formpanel)
        self.formpanel.Destroy()

        form_spec = analyzer_desc.clazz.create_config_form(self.ctx)
        self.formpanel = frm.Form(self, form_spec)

        save_config_btn = wx.Button(self.formpanel, -1, "Save Config", (380, 10))

        self.vsizer.Add(
            self.formpanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=5
        )
        self.vsizer.Layout()

        self.cur_filters_list_box.Clear()
        self.cur_indices_list_box.Clear()
        filters = self.ctx.get_selected_filters()
        indices = self.ctx.get_selected_index_paths()
        if len(filters) > 0:
            self.cur_filters_list_box.InsertItems(self.ctx.get_selected_filters(), pos=0)
        if len(indices) > 0:
            self.cur_indices_list_box.InsertItems(self.ctx.get_selected_index_paths(), pos=0)

        self.Bind(wx.EVT_BUTTON, self.run_save_config, save_config_btn)
        self.ctx.get_server().trigger_update()
        self.update_flag = True
        self.on_form_update(None)

    def update(self):
        self.update_impl(None)

    def _md_report_prelude(self, analyzer_desc, mdoutput: MarkdownDocument):
        mdoutput.write_h1("Test: " + analyzer_desc.display_name)
        mdoutput.write_h3("Applied to indices: ")
        mdoutput.write_bullet_points(self.ctx.get_selected_index_paths())
        filters = [
            reg.session_filter_registry[filter_name]
            for filter_name in self.ctx.get_selected_filters()
        ]

        if len(filters) > 0:
            mdoutput.write_h3("Patients must satisfy: ")
            mdoutput.write_bullet_points([flt.display_name for flt in filters])

        mdoutput.write_paragraph()

    def run_save_config(self, event):
        section_name = self.get_current_analyzer_desc().name
        config_to_save = self.get_current_config_for_analyzer()

        config = configparser.RawConfigParser()
        config.read('src/analyzers/analyzers.cfg')
        for cfg in config_to_save:
            config.set(section_name, cfg, config_to_save[cfg])

        with open('src/analyzers/analyzers.cfg', 'w') as configfile:
            config.write(configfile)

    def clear_md_report(self, event):
        self.ctx.set_current_report(MarkdownDocument())
        self.ctx.get_server().trigger_update()

    def run_analyzer(self, mdoutput=None) -> MarkdownDocument:
        analyzer_desc = self.get_current_analyzer_desc()

        analyzer: AbstractAnalyzer = analyzer_desc.clazz(self.ctx, self.get_current_config_for_analyzer())

        if mdoutput is None:
            mdoutput = MarkdownDocument()
        analyzer.process(self.ctx.create_active_dataframe())
        self._md_report_prelude(analyzer_desc, mdoutput)
        analyzer.present_as_markdown(mdoutput)
        return mdoutput

    def add_to_report(self, event):
        self.run_analyzer(self.ctx.get_current_report())
        self.ctx.get_server().trigger_update()
