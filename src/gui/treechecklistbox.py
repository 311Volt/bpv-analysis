import typing

import wx
import wx.lib.agw.customtreectrl as wxtree

from src.gui.checklistentry import CheckListEntry


class TreeCheckListBox(wxtree.CustomTreeCtrl):

    def __init__(self, parent, **kwargs):
        super().__init__(parent=parent, style=wx.BORDER_SUNKEN, **kwargs)
        self.root = self.AddRoot("BPV indices")
        self.group_items: typing.List[wxtree.GenericTreeItem] = []
        self.child_items: typing.List[wxtree.GenericTreeItem] = []

        self.Bind(wxtree.EVT_TREE_ITEM_CHECKED, self.update_3_state)

    def add_item_group(self, parent_item: CheckListEntry, items: typing.List[CheckListEntry]):
        group_parent = self.AppendItem(self.root, parent_item.display_name, ct_type=1)
        group_parent.Set3State(True)
        self.group_items.append(group_parent)
        for item in items:
            child = self.AppendItem(group_parent, item.display_name, data=item.name, ct_type=1)
            self.child_items.append(child)
        self.Expand(self.root)
        group_parent.Expand()

    def update_3_state(self, event: wxtree.TreeEvent):
        item: wxtree.GenericTreeItem = event.GetItem()
        if item.Is3State():
            self.sync_children_to_3state(item)
        else:
            self.sync_3state_to_children(item)
        event.Skip()

    def sync_children_to_3state(self, item):
        if item.Get3StateValue() == wx.CHK_CHECKED:
            self.CheckChilds(item, True)
        elif item.Get3StateValue() == wx.CHK_UNCHECKED:
            self.CheckChilds(item, False)

    def sync_3state_to_children(self, item):
        parent: wxtree.GenericTreeItem = item.GetParent()
        children = parent.GetChildren()
        total = len(children)
        checked = sum(child.IsChecked() for child in children)
        self.CheckItem(parent, wx.CHK_UNDETERMINED)
        if checked == 0:
            self.CheckItem(parent, wx.CHK_UNCHECKED)
        elif checked == total:
            self.CheckItem(parent, wx.CHK_CHECKED)

    def get_selections(self):
        return [item.GetData() for item in self.child_items if item.IsChecked()]

    def set_selections(self, selection_paths: typing.Iterable[str]):
        selection_paths_set = set(selection_paths)
        for item in self.child_items:
            self.CheckItem(item, item.GetData() in selection_paths_set)

    
