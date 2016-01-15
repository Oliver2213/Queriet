import wx

class Options(wx.Frame):
	def __init__(self, parent, title):
		super(Options, self).__init__(parent, title=title)
		self.SetupUI()
		self.Center()
		self.Show()

	def SetupUI(self):
		panel = wx.Panel(self)
		vertical = wx.BoxSizer(wx.VERTICAL)
		for c in self.config:
			h = wx.BoxSizer(wx.HORIZONTAL)
			field = wx.StaticText(panel, -1, c, size=(90, 30))
			InputBox = wx.TextCtrl(panel, -1, size=(100, 30))
			h.Add(field, 1, wx.LEFT, 10)
			h.Add(InputBox, 5, wx.EXPAND, 10)
			vertical.Add(h, 1, wx.EXPAND)
			vertical.AddSpacer(10,20)
		panel.SetSizer(vertical)


app = wx.App()
options = Options(None, "Test UI")
app.MainLoop()