import wx

import src.registry as reg
import src.dataflow.indexpath as idxpath
import src.datareader as datareader
import src.dataflow.dataextractor as extractor

import webbrowser

class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(640, 360))
        self.SetBackgroundColour(wx.NullColour)

        index_choices = [idx.display_name for idx in reg.arr_patient_indices_registry]
        filter_choices = [flt.display_name for flt in reg.arr_session_filter_registry]
        extractor_choices = [xt.display_name for xt in reg.arr_series_extractor_registry]

        self.index_checkboxes = wx.CheckListBox(
            parent=self, choices=index_choices, pos=(30, 30), size=(160, 200)
        )
        self.filter_checkboxes = wx.CheckListBox(
            parent=self, choices=filter_choices, pos=(200, 30), size=(160, 200)
        )
        self.extractor_checkboxes = wx.CheckListBox(
            parent=self, choices=extractor_choices, pos=(370, 30), size=(160, 200)
        )

        # self.index_checkboxes.SetCheckedItems(range(len(index_choices)))
        # self.filter_checkboxes.SetCheckedItems(range(len(filter_choices)))
        # self.extractor_checkboxes.SetCheckedItems(range(len(extractor_choices)))
        self.index_checkboxes.SetCheckedItems([0, 1, 2])
        self.extractor_checkboxes.SetCheckedItems([0])

        self.open_preview_btn = wx.Button(self, -1, "Open Preview", pos=(30, 265), size=(160, 24))
        self.gen_markdown_btn = wx.Button(self, -1, "Generate Markdown", pos=(30, 295), size=(160, 24))
        self.gen_markdown_btn.Disable()

        self.Bind(wx.EVT_BUTTON, self.show_preview, self.open_preview_btn)

        self.txr_sessions = datareader.batch_import_txr_sessions("RESP_metadata.csv")

    def get_selected_index_names(self):
        return [
            reg.arr_patient_indices_registry[chkboxidx].name
            for chkboxidx in self.index_checkboxes.GetCheckedItems()
        ]

    def get_selected_filter_names(self):
        return [
            reg.arr_session_filter_registry[chkboxidx].name
            for chkboxidx in self.filter_checkboxes.GetCheckedItems()
        ]

    def get_selected_extractor_names(self):
        return [
            reg.arr_series_extractor_registry[chkboxidx].name
            for chkboxidx in self.extractor_checkboxes.GetCheckedItems()
        ]

    def list_selected_index_paths(self):
        return idxpath.create_combination_paths(
            self.get_selected_extractor_names(),
            self.get_selected_index_names()
        )

    def show_preview(self, event):
        df = extractor.create_data_frame(
            sessions=self.txr_sessions,
            filter_names=self.get_selected_filter_names(),
            index_paths=self.list_selected_index_paths()
        )
        with open("bpframe.html", "w") as htmlfile:
            htmlfile.write(df.to_html())
            webbrowser.open("bpframe.html")
        pass

    def generate_markdown(self, event):
        pass
