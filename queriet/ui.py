#Queriet user interface file
#Please see the license file in the main directory for licensing information

import os
import wx
import utils

class MainUI(wx.Frame):
	"""Class that holds the main user interface for Queriet"""
	def __init__(self, controller, parent, title):
		super(MainUI, self).__init__(parent, title=title, size=(1000, 800))
		self.controller = controller
		self.setup()
		
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.CreateIcon()
		self.Center()
		self.Show()

	def setup(self):
		"""Sets up the application UI layout and manu bar"""
		self.panel = wx.Panel(self) # the main pannel that children pannels inherit from

		self.menubar = wx.MenuBar()
		

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

	def CreateIcon(self):
		"""Creates the system tray icon."""
		self.icon = SystemTrayIcon(UI=self, text="Queriet")


	def showhide(self, event):
		if self.Shown:
			self.Hide()
		else:
			self.Show()

	def OpenSite(self, event):
		"""Opens the Queriet website"""
		os.startfile('https://github.com/oliver2213/queriet')

	def OnClose(self, event):
		"""Delete system tray icon and this window."""
		self.icon.Destroy()
		self.Destroy()


class SystemTrayIcon(wx.TaskBarIcon):
	"""Class that implements a system tray icon for Queriet"""

	def __init__(self, UI, text):
		"""This is the initialization for the system tray icon class. It creates the menus for use in CreatePopupMenu, and PopupMenu. It also gets passed the MainUI object so it can call it's methods for menu items."""
		super(SystemTrayIcon, self).__init__()
		self.MUI = UI
		self.SetIcon(wx.NullIcon, text)
		self.CreateMenu()
		self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

	def CreateMenu(self):
		#Create our menu now, so we can reuse it later
		self.menu = wx.Menu()
		self.showhide_item = utils.CreateMenuItem(self.menu, '&show or hide Queriet', self.MUI.showhide)
		self.openSite_item = utils.CreateMenuItem(self.menu, 'Open the Queriet &website', self.MUI.OpenSite)
		self.menu.AppendSeparator()
		self.exit_item = utils.CreateMenuItem(self.menu, 'e&xit', self.OnClose)

	def CreatePopupMenu(self):
		"""Show the menu."""
		self.PopupMenu(self.menu)

	def on_left_down(self, event):
		"""When the system tray icon is left clicked, show / hide the main interface"""
		self.MUI.showhide(None) # it expects to be passed an event object, so we use none

	def OnClose(self, event):
		wx.CallAfter(self.MUI.controller.close) #Run the top-level close method instead of just the UI's one, so other resources can be released if needed
