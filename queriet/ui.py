#Queriet user interface file
#Please see the license file in the main directory for licensing information

import wx

class mainUI(wx.Frame):
	def __init__(self, parent, title):
		super(mainUI, self).__init__(parent, title=title, size=(1000, 800))
		self.setup()
		self.Center()
		self.Show()

	def setup(self):
		panel = wx.Panel(self) # the main pannel that children pannels inherit from

		#API list
		listPanel = wx.Panel(panel)
		listSizer = wx.BoxSizer(wx.HORIZONTAL) #A list to hold the API listview
		apiStatic = wx.StaticText(listPanel, -1, 'API') #A label for our listview
		listSizer.Add(apiStatic, 1, wx.TOP | wx.BOTTOM | wx.LEFT, 5) # adding this label to our api sizer
		self.apiList = wx.ListBox(listPanel, -1) #create the actual list
		listSizer.Add(self.apiList, 1, wx.EXPAND | wx.ALL, 20) #Add it to the list sizer

		#Info panel
		infoPanel = wx.Panel(panel)
		infoSizer = wx.BoxSizer(wx.VERTICAL)

		#Input panel.
		inputPanel = wx.Panel(infoPanel)
		inputStatic = wx.StaticText(inputPanel, -1, 'Search term or equation')
		self.input = wx.TextCtrl(inputPanel, -1)
		self.searchButton = wx.Button(inputPanel, -1, 'Search', size=(90, 30))
		inputSizer = wx.BoxSizer(wx.HORIZONTAL)
		inputSizer.Add(inputStatic, 1, wx.TOP|wx.LEFT|wx.BOTTOM, 5)
		inputSizer.Add(self.input, 3, wx.TOP|wx.BOTTOM, 10)
		inputSizer.Add(self.searchButton, 2, wx.TOP|wx.RIGHT|wx.BOTTOM, 20)

		#Output panel
		outputPanel = wx.Panel(infoPanel)
		outputSizer = wx.BoxSizer(wx.VERTICAL)
		outputStatic = wx.StaticText(outputPanel, -1, 'results', (5, 5))
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
mainUI(None, "Queriet")
app.MainLoop()