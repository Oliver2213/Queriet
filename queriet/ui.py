import wx

class main(wx.Frame):
	def __init__(self, parent, title):
		super(main, self).__init__(parent, title=title, size=(1000, 800))
		self.setup()
		self.Center()
		self.Show()

	def setup(self):
		panel = wx.Panel(self)
		listPanel = wx.Panel(panel)
		listSizer = wx.BoxSizer(wx.VERTICAL)
		apiStatic = wx.StaticText(listPanel, -1, 'API', (5, 5))
		listSizer.Add(apiStatic, 1, wx.TOP | wx.BOTTOM | wx.LEFT, 5)
		self.apiList = wx.ListBox(listPanel, -1)
		listSizer.Add(self.apiList, 1, wx.EXPAND | wx.ALL, 20)
		infoPanel = wx.Panel(panel)
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		mainSizer.Add(listPanel, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 30)
		mainSizer.Add(infoPanel, 5, wx.EXPAND|wx.ALL, 30)


app = wx.App()
main(None, "Test UI")
app.MainLoop()