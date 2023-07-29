import wx

import src.registry as reg



class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(640, 360))

        index_choices = [idx.display_name for idx in reg.arr_patient_indices_registry]
        filter_choices = [flt.display_name for flt in reg.arr_session_filter_registry]
        extractor_choices = [xt.display_name for xt in reg.arr_series_extractor_registry]

        self.index_checkboxes = wx.CheckListBox(
            parent=self, choices=index_choices, pos=(30, 20), size=(160, 200)
        )
        self.filter_checkboxes = wx.CheckListBox(
            parent=self, choices=filter_choices, pos=(200, 20), size=(160, 200)
        )
        self.extractor_checkboxes = wx.CheckListBox(
            parent=self, choices=extractor_choices, pos=(370, 20), size=(160, 200)
        )

        self.open_preview_btn = wx.Button(self, -1, "Show Preview", pos=(30, 245), size=(160, 24))
        self.gen_markdown_btn = wx.Button(self, -1, "Generate Markdown", pos=(30, 275), size=(160, 24))

    def show_preview(self):
        pass

    def generate_markdown(self):
        pass
