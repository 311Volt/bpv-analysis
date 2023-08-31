import typing
from dataclasses import dataclass
from src.gui.checklistentry import CheckListEntry

import wx


class RegCheckListBox(wx.CheckListBox):
    def __init__(self, parent: wx.Window, entries: typing.List[CheckListEntry], **kwargs):
        self.entries = entries

        self.ctrl_choices = [entry.display_name for entry in entries]
        self.entry_to_index = {entry.name: idx for idx, entry in enumerate(entries)}
        self.index_to_entry = [entry.name for entry in entries]

        super().__init__(parent=parent, choices=self.ctrl_choices, **kwargs)

    def get_selections(self):
        return [self.index_to_entry[idx] for idx in self.GetCheckedItems()]

    def set_selections(self, entry_names: typing.List[str]):
        self.SetCheckedItems([self.entry_to_index[name] for name in entry_names])

