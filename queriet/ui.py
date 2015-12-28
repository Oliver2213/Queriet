#Queriet user interface file
#Please see the license file in the main directory for licensing information

import wx
import utils

class mainUI(wx.Frame):
	"""Class that holds the main user interface for Queriet"""
	def __init__(self, parent, title):
		super(mainUI, self).__init__(parent, title=title, size=(1000, 800))
		self.setup()
		self.Center()
		self.Show()

	def setup(self):
		"""Sets up the application UI layout"""
		self.panel = wx.Panel(self) # the main pannel that children pannels inherit from

		#API list
		self.listPanel = wx.Panel(self.panel)
		self.listSizer = wx.BoxSizer(wx.HORIZONTAL) #A list to hold the different APIs
		self.apiStatic = wx.StaticText(self.listPanel, -1, 'API') #A label for our listview
		self.listSizer.Add(self.apiStatic, 1, wx.TOP | wx.BOTTOM | wx.LEFT, 5) # adding this label to our api sizer
		self.apiList = wx.ListBox(self.listPanel, -1) #create the actual list
		self.listSizer.Add(self.apiList, 1, wx.EXPAND | wx.ALL, 20) #Add it to the list sizer

		#Info panel, holds input and output pannels
		self.infoPanel = wx.Panel(self.panel)
		self.infoSizer = wx.BoxSizer(wx.VERTICAL)

		#Input panel, used for inputting information for a query, can be API defined
		self.inputPanel = wx.Panel(self.infoPanel)
		self.inputStatic = wx.StaticText(self.inputPanel, -1, 'Search term or equation')
		self.input = wx.TextCtrl(self.inputPanel, -1)
		self.searchButton = wx.Button(self.inputPanel, -1, 'Search', size=(90, 30))
		self.inputSizer = wx.BoxSizer(wx.HORIZONTAL) # A sizer for items in the input panel
		self.inputSizer.Add(self.inputStatic, 1, wx.TOP|wx.LEFT|wx.BOTTOM, 5) # adding out input label
		self.inputSizer.Add(self.input, 3, wx.TOP|wx.BOTTOM, 10)
		self.inputSizer.Add(self.searchButton, 2, wx.TOP|wx.RIGHT|wx.BOTTOM, 20)

		#Output panel
		self.outputPanel = wx.Panel(self.infoPanel)
		self.outputSizer = wx.BoxSizer(wx.VERTICAL)
		self.outputStatic = wx.StaticText(self.outputPanel, -1, 'results', (5, 5))
		self.output = wx.TextCtrl(self.outputPanel, -1, style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.outputSizer.Add(self.outputStatic, 0, wx.TOP|wx.LEFT, 10)
		self.outputSizer.Add(self.output, 6, wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.EXPAND, 20)

		#Add our input and output pannels to the info panel sizer
		self.infoSizer.Add(self.inputPanel, 1, wx.TOP|wx.LEFT|wx.RIGHT, 20)
		self.infoSizer.Add(self.outputPanel, 3, wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.EXPAND, 30)


		#main
		self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.mainSizer.Add(self.listPanel, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 30)
		self.mainSizer.Add(self.infoPanel, 5, wx.EXPAND|wx.ALL, 30)

		#Setting sizers
		self.panel.SetSizer(self.mainSizer)
		self.listPanel.SetSizer(self.listSizer)
		self.inputPanel.SetSizer(self.inputSizer)
		self.outputPanel.SetSizer(self.outputSizer)
		self.infoPanel.SetSizer(self.infoSizer)

class SystemTrayIcon(wx.TaskBarIcon):
	"""Class that implements a system tray icon fir Queriet"""

	def __init__(self, MainUI):
		"""This is the initialization for the system tray icon class. It creates the menus for use in CreatePopupMenu, and PopupMenu. It also gets passed the MainUI object so it can call it's methods for menu items."""
		super(SystemTrayIcon, self).__init__()
		self.MUI=MainUI
		#Create our menu now, so we can reuse it later
		self.menu=wx.Menu()
		utils.CreateMenuItem(self.menu, 'show / hide Queriet', self.MUI.showhide)
		self.menu.AppendSeparator()
		utils.CreateMenuItem(self.menu, 'e&xit', self.MUI.Exit())

	def CreatePopupMenu(self):
		"""Return our menu"""
		return self.menu

def test():
	app = wx.App()
	mainUI(None, "Queriet")
	app.MainLoop()