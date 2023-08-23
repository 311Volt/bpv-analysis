import wx


class SubWindow(wx.Frame):

    def __init__(self, parent, **kwargs):

        self.on_close_callback = kwargs.get("on_close_callback")
        kwargs.pop("on_close_callback", None)
        super().__init__(parent, **kwargs)
        if self.on_close_callback is None:
            self.on_close_callback = lambda: ()
        self.SetBackgroundColour(wx.NullColour)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.on_close_callback()
        self.Destroy()
