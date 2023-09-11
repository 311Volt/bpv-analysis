import typing
from dataclasses import dataclass

from wx.lib.masked.numctrl import NumCtrl


@dataclass
class Number:
    key: str
    min_value: typing.Optional[float] = None
    max_value: typing.Optional[float] = None
    initial_value: typing.Optional[float] = None

    def create_wx_control(self, parent, **kw) -> NumCtrl:
        ctrl = NumCtrl(parent, **kw)
        ctrl.SetMin(self.min_value)
        ctrl.SetMax(self.max_value)
        if self.initial_value is not None:
            ctrl.SetValue(self.initial_value)
        return ctrl

    def get_value_from_control(self, control: NumCtrl):
        return control.GetValue()

