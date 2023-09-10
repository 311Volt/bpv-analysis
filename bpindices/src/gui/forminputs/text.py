from dataclasses import dataclass

import wx

@dataclass
class Text:
    key: str
    initial_value: str

    def create_wx_control(self, parent, **kw) -> wx.TextCtrl:
        return wx.TextCtrl(parent, value=self.initial_value, **kw)

    def get_value_from_control(self, control: wx.TextCtrl):
        return control.GetLineText(0)

