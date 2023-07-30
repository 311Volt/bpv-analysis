import wx


class RegCheckListBox(wx.CheckListBox):
    def __init__(self, parent, **kwargs):
        wx.CheckListBox.__init__(self, parent, *kwargs)

