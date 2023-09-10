import typing
from dataclasses import dataclass

import wx


@dataclass
class SubsetOf:
    key: str
    choices: typing.List[str]
    select_all_by_default: bool = False

    def create_wx_control(self, parent, **kw) -> wx.CheckListBox:
        ctrl = wx.CheckListBox(
            parent,
            choices=self.choices,
            style=wx.BORDER_SUNKEN,
            **kw
        )
        if self.select_all_by_default:
            ctrl.SetCheckedItems(range(len(self.choices)))
        return ctrl

    def get_value_from_control(self, control: wx.CheckListBox):
        return [self.choices[idx] for idx in control.GetCheckedItems()]

