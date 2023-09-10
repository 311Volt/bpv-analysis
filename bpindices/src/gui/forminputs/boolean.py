from dataclasses import dataclass

import wx


@dataclass
class Boolean:
    key: str
    initial_value: bool = False

    def create_wx_control(self, parent, **kw) -> wx.CheckBox:
        chkbox = wx.CheckBox(parent, **kw)
        chkbox.SetValue(self.initial_value)
        return chkbox

    def get_value_from_control(self, control: wx.CheckBox):
        return control.IsChecked()
