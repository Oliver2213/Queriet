import wx

class main(wx.Frame):
	def __init__(self, parent, title):
		super(main, self).__init__(parent, title=title, size=(1000, 800))
		self.setup()
		self.Center()
		self.Show()

	def setup(self):
		panel = wx.Panel(self)

		#API list
		listPanel = wx.Panel(panel)
		listSizer = wx.BoxSizer(wx.HORIZONTAL)
		apiStatic = wx.StaticText(listPanel, -1, 'API')
		listSizer.Add(apiStatic, 1, wx.TOP | wx.BOTTOM | wx.LEFT, 5)
		self.apiList = wx.ListBox(listPanel, -1)
		listSizer.Add(self.apiList, 1, wx.EXPAND | wx.ALL, 20)

		#Info panel
		infoPanel = wx.Panel(panel)
		infoSizer = wx.BoxSizer(wx.VERTICAL)

		#Input panel.
		inputPanel = wx.Panel(infoPanel)
		inputStatic = wx.StaticText(inputPanel, -1, 'Input')
		self.input = wx.TextCtrl(inputPanel, -1)
		self.searchButton = wx.Button(inputPanel, -1, 'Search', size=(90, 30))
		inputSizer = wx.BoxSizer(wx.HORIZONTAL)
		inputSizer.Add(inputStatic, 1, wx.TOP|wx.LEFT|wx.BOTTOM, 5)
		inputSizer.Add(self.input, 3, wx.TOP|wx.BOTTOM, 10)
		inputSizer.Add(self.searchButton, 2, wx.TOP|wx.RIGHT|wx.BOTTOM, 20)

		#Output panel
		outputPanel = wx.Panel(infoPanel)
		outputSizer = wx.BoxSizer(wx.VERTICAL)
		outputStatic = wx.StaticText(outputPanel, -1, 'Output', (5, 5))
		self.output = wx.TextCtrl(outputPanel, -1, style=wx.TE_MULTILINE|wx.TE_READONLY)
		outputSizer.Add(outputStatic, 0, wx.TOP|wx.LEFT, 10)
		outputSizer.Add(self.output, 6, wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.EXPAND, 20)

		infoSizer.Add(inputPanel, 1, wx.TOP|wx.LEFT|wx.RIGHT, 20)
		infoSizer.Add(outputPanel, 3, wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.EXPAND, 30)


		#main
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		mainSizer.Add(listPanel, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 30)
		mainSizer.Add(infoPanel, 5, wx.EXPAND|wx.ALL, 30)

		#Setting sizers
		panel.SetSizer(mainSizer)
		listPanel.SetSizer(listSizer)
		inputPanel.SetSizer(inputSizer)
		outputPanel.SetSizer(outputSizer)
		infoPanel.SetSizer(infoSizer)




app = wx.App()
main(None, "Test UI")
app.MainLoop()