import src.gui.form as frm
import wx

import src.registry as reg


class AnalyzerLauncher(wx.Frame):
    def __init__(self, parent, ctx, **kwargs):
        super().__init__(parent, **kwargs)

        self.vsizer = wx.BoxSizer(wx.VERTICAL)

        self.ctrlpanel = wx.Panel(self, style=wx.BORDER_SUNKEN)
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

        self.vsizer.Add(
            self.ctrlpanel, flag=wx.EXPAND | wx.ALL, border=5
        )
        self.vsizer.Add(
            self.formpanel, flag=wx.EXPAND | wx.ALL, border=5
        )

        self.update_analyzer_choice(None)
        self.SetSizer(self.vsizer)
        self.Bind(wx.EVT_BUTTON, self.run_analyzer, self.run_analyzer_btn)
        self.Bind(wx.EVT_COMBOBOX, self.update_analyzer_choice, self.analyzer_choice)

    def get_current_analyzer_desc(self):
        return reg.arr_analyzer_registry[self.analyzer_choice.GetSelection()]

    def get_current_config_for_analyzer(self):
        return self.formpanel.collect()

    def update_analyzer_choice(self, event):
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

    def run_analyzer(self, event):
        analyzer_desc = self.get_current_analyzer_desc()

        analyzer = analyzer_desc.clazz(self.ctx, self.get_current_config_for_analyzer())
        analyzer.process()
        analyzer.present()



