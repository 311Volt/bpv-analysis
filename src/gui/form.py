import typing

import wx
import wx.lib.scrolledpanel as scrolled


class Form(scrolled.ScrolledPanel):

    def __init__(self, parent, forminputs, **kwargs):
        super().__init__(parent, style=wx.BORDER_SUNKEN, **kwargs)

        self.sizer = wx.GridBagSizer(9, 4)
        self.forminputs = forminputs
        self.onchange = lambda: None

        self.controls: typing.List[wx.Window] = []

        for idx, forminput in enumerate(forminputs):
            ctrl: wx.Window = forminput.create_wx_control(self)
            label = wx.StaticText(self, label=forminput.key, style=wx.ALIGN_RIGHT)

            flag_top = wx.TOP if idx == 0 else 0
            self.sizer.Add(
                label,
                pos=wx.GBPosition(row=idx, col=0),
                flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.LEFT | flag_top,
                border=6
            )
            self.sizer.Add(
                ctrl,
                pos=wx.GBPosition(row=idx, col=1),
                flag=flag_top,
                border=6
            )
            self.controls.append(ctrl)


        self.SetSizer(self.sizer)
        self.SetupScrolling()

    def _on_change(self, event):
        self.onchange()

    def collect(self):
        result_dict = dict()
        for forminput, inputctrl in zip(self.forminputs, self.controls):
            result_dict[forminput.key] = forminput.get_value_from_control(inputctrl)
        return result_dict




