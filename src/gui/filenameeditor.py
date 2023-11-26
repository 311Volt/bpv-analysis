import wx
from src.bpvappcontext import BPVAppContext


class FilenameEditor(wx.Frame):
    def __init__(self, parent, ctx: BPVAppContext, **kwargs):
        super().__init__(parent, **kwargs)

        self.vsizer = wx.BoxSizer(wx.VERTICAL)

        self.ctrlpanel = wx.Panel(self, style=wx.BORDER_SUNKEN)
        self.ctx = ctx

        self.label_analyzer_choice = wx.StaticText(
            self.ctrlpanel, label="Report filename: ",
            pos=(10, 7)
        )
        self.filename_change = wx.TextCtrl(
            self.ctrlpanel,
            name="Filename",
            value=self.ctx.get_report_filename(),
            pos=(110, 5)
        )
        self.set_report_filename_btn = wx.Button(self.ctrlpanel, -1, "Set", pos=(150, 30))

        self.statussizer = wx.BoxSizer(wx.HORIZONTAL)

        self.vsizer.Add(
            self.ctrlpanel, flag=wx.EXPAND | wx.ALL, border=5
        )

        self.SetSizer(self.vsizer)
        self.Bind(wx.EVT_BUTTON, self.set_report_filename, self.set_report_filename_btn)

    def set_report_filename(self, event):
        self.ctx.set_report_filename(self.filename_change.GetValue())
        self.ctx.set_clear_report(True)
        self.Close()
