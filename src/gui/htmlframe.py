import markdown
import wx
import wx.html


class HtmlFrame(wx.Frame):
    def __init__(self, parent, **kwargs):
        wx.Frame.__init__(self, parent, -1, **kwargs)
        self.html = wx.html.HtmlWindow(self)
        if "gtk2" in wx.PlatformInfo:
            self.html.SetStandardFonts()


        self.html.SetPage("")

    def set_page(self, source: str):
        self.html.SetPage(source)

    def set_markdown(self, md: str):
        self.set_page(markdown.markdown(md, extensions=['tables']))
