import wx

import src.gui.form as frm
import src.registry as reg


class AnalyzerLauncher(wx.Frame):
    def __init__(self, parent, ctx, **kwargs):
        super().__init__(parent, **kwargs)

        self.vsizer = wx.BoxSizer(wx.VERTICAL)

        self.ctrlpanel = wx.Panel(self, style=wx.BORDER_SUNKEN)
        self.statuspanel = wx.Panel(self, style=wx.BORDER_SUNKEN)
        self.formpanel: frm.Form = wx.Panel(self)
        self.ctx = ctx

        self.label_analyzer_choice = wx.StaticText(
            self.ctrlpanel, label="Analyzer: ",
            pos=(10, 10)
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
        self.run_analyzer_btn = wx.Button(self.ctrlpanel, -1, "Run...", pos=(170, 5))

        self.cur_indices_list_box = wx.ListBox(
            self.statuspanel, size=(200, 100),
            choices=ctx.get_selected_index_paths()
        )
        self.cur_filters_list_box = wx.ListBox(
            self.statuspanel, size=(200, 100),
            choices=ctx.get_selected_filters()
        )

        self.statussizer = wx.BoxSizer(wx.HORIZONTAL)
        self.statussz1 = wx.StaticBoxSizer(wx.VERTICAL, self.statuspanel, "Using indices: ")
        self.statussz1.Add(self.cur_indices_list_box, border=5)
        self.statussz2 = wx.StaticBoxSizer(wx.VERTICAL, self.statuspanel, "Using filters: ")
        self.statussz2.Add(self.cur_filters_list_box, border=5)

        self.chk_rerun_on_upd = wx.CheckBox(self.ctrlpanel, label="Re-run on update", pos=(270, 10))
        self.chk_rerun_on_upd.SetValue(False)
        self.chk_rerun_on_upd.Enable(False)

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
        self.Bind(wx.EVT_BUTTON, self.run_analyzer, self.run_analyzer_btn)
        self.Bind(wx.EVT_COMBOBOX, self.update_impl, self.analyzer_choice)

    def get_current_analyzer_desc(self):
        return reg.arr_analyzer_registry[self.analyzer_choice.GetSelection()]

    def get_current_config_for_analyzer(self):
        return self.formpanel.collect()

    def update_impl(self, event):
        analyzer_desc = self.get_current_analyzer_desc()
        analyzer_name = analyzer_desc.name

        self.vsizer.Detach(self.formpanel)
        self.formpanel.Destroy()

        form_spec = analyzer_desc.clazz.create_config_form(self.ctx)
        self.formpanel = frm.Form(self, form_spec)
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

        if self.chk_rerun_on_upd.GetValue():
            self.run_analyzer(None)

    def update(self):
        self.update_impl(None)

    def run_analyzer(self, event):
        analyzer_desc = self.get_current_analyzer_desc()

        analyzer = analyzer_desc.clazz(self.ctx, self.get_current_config_for_analyzer())

        analyzer.process(self.ctx.create_active_dataframe())
        analyzer.present()



