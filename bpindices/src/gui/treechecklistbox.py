import wx
import typing
import wx.lib.agw.customtreectrl
from src.gui.checklistentry import CheckListEntry


class TreeCheckListBox(wx.lib.agw.customtreectrl.CustomTreeCtrl):

    def __init__(self, parent, **kwargs):
        super().__init__(parent=parent, **kwargs)
        pass

    def add_item_group(self, parent_item: CheckListEntry, items: typing.List[CheckListEntry]):
        pass

    
