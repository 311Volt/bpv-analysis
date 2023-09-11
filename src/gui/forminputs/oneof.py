import typing
from dataclasses import dataclass

import wx


@dataclass
class OneOf:
    key: str
    choices: typing.List[str]
    default_choice_str: str = ""

    def create_wx_control(self, parent, **kw) -> wx.ComboBox:
        ctrl = wx.ComboBox(
            parent,
            choices=self.choices,
            value=self.default_choice_str,
            style=wx.CB_READONLY | wx.CB_DROPDOWN,
            **kw
        )
        if self.default_choice_str == "":
            ctrl.SetValue(self.choices[0])
        return ctrl

    def get_value_from_control(self, control: wx.ComboBox):
        return control.GetValue()

