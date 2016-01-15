#Queriet user interface file
#Please see the license file in the main directory for licensing information

import logging
import os
import wx
import utils
import info

class MainUI(wx.Frame):
	"""Class that holds the main user interface for Queriet"""
	def __init__(self, controller, parent, title):
		super(MainUI, self).__init__(parent, title=title, size=(1000, 800))
		self.log = logging.getLogger('Queriet.'+__name__)
		self.log.info("User interface starting up.")
		self.controller = controller
		self.setup()
		self.SetupMenuBar()
		self.Bind(wx.EVT_CLOSE, self.controller.OnClose)
		self.CreateIcon()
		self.Center()
		self.Show()

	def setup(self):
		"""Sets up the application UI layout and menu bar"""
		self.log.debug("Setting up main UI...")

		self.ListSizer = wx.BoxSizer(wx.HORIZONTAL) #A list to hold the different APIs
		self.MainSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.CurrentPlugin = None
		self.CurrentPluginNumber = -1
		self.InfoPanel = None
		self.panel = wx.Panel(self) # the main pannel that children pannels inherit from

		#API list
		self.ListPanel = wx.Panel(self.panel)

		self.apiStatic = wx.StaticText(self.ListPanel, -1, 'API') #A label for our listview

		self.apiList = wx.ListBox(self.ListPanel, -1) #create the actual list
		self.apiList.Bind(wx.EVT_LISTBOX, self.OnListChange)

		#Setting sizers
		self.SetSizers()
		self.log.debug("Done!")

	def SetSizers(self):
		self.MainSizer.Clear()
		self.listSizer.Clear()

		self.ListSizer.Add(self.apiStatic, 1, wx.EXPAND) # adding this label to our api sizer
		self.ListSizer.Add(self.apiList, 3, wx.EXPAND) #Add it to the list sizer
		self.ListSizer.Layout()
		self.ListSizer.Fit()
		self.ListPanel.SetSizer(self.ListSizer)
		self.MainSizer.Add(self.ListPanel, 1)
		if self.InfoPanel:
			self.MainSizer.Add(self.InfoPanel, 3, wx.EXPAND)
		self.MainSizer.Layout()
		self.MainSizer.fit()
		self.panel.SetSizer(self.MainSizer)


	def SetupMenuBar(self):
		"""Setup our menubar.
			Menu bar menus as well as items should be named like: self.MenuBar_file (the file, menu), self.MenuBar_file_exit (an exit item in the file menu)
		"""
		self.log.debug("Setting up menu bar...")
		try:
			self.MenuBar = wx.MenuBar()
			self.MenuBar_file = wx.Menu()
			self.MenuBar_file_exit = utils.CreateMenuItem(self.MenuBar_file, 'E&xit', self.controller.OnClose, id=wx.ID_EXIT)
			
			self.MenuBar.Append(self.MenuBar_file, '&File')
			self.MenuBar_help = wx.Menu()
			self.MenuBar_help_about = utils.CreateMenuItem(self.MenuBar_help, "&About...", self.OnAbout, id=wx.ID_ABOUT)
			self.MenuBar_help_OpenSite = utils.CreateMenuItem(self.MenuBar_help, 'Open Queriet &site...', self.OpenSite)
			self.MenuBar_help_OpenIssuePage = utils.CreateMenuItem(self.MenuBar_help, 'File an &issue...', self.OpenIssuePage)
			self.MenuBar.Append(self.MenuBar_help, '&Help')
			self.SetMenuBar(self.MenuBar)
		except:
			self.log.exception("Error setting up menu bar!")
		self.log.debug("Done!")

	def SetInfoPanel(self, info):
		"""This method sets the info panel object."""
		self.log.debug("Setting the info panel.\nProvided panel is %s" %(info))
		if self.InfoPanel:
			self.log.debug("Existing info panel %s, hiding it." %(self.InfoPanel))
			self.InfoPanel.Hide()
		self.InfoPanel = info
		self.SetSizers()
		self.log.debug("Set new info panel.")

	def CreateIcon(self):
		"""Creates the system tray icon."""
		self.log.debug("Creating system tray icon...")
		self.icon = SystemTrayIcon(UI=self, text="Queriet")
		self.log.debug("Done!")

	def SetFocus(self, value):
		"""Change the displayed UI to that of the selected plugin. Do not pass this function a value less than 0."""
		if value<0 or value == self.CurrentPluginNumber:
			return
		plugin = self.apiList.GetClientData(self.apiList.GetSelection())
		if not plugin:
			return
		if self.CurrentPlugin:
			try:
				self.CurrentPlugin.OnLoseFocus()
			except:
				self.log.exception("Error while running OnLoseFocus method of plugin!")
		self.CurrentPlugin = plugin
		self.CurrentPluginNumber = value
		try:
			self.SetInfoPanel(plugin.InfoPanel)
		except:
			self.log.exception("Error setting plugin info panel!")
		try:
			plugin.OnGainFocus()
		except:
			self.log.exception("Error while running OnGainFocus method of plugin!")

	def showhide(self, event=None):
		if self.Shown:
			self.Hide()
			self.log.debug("Hid main window.")
		else:
			self.Show()
			self.log.debug("Showed window.")

	def OpenSite(self, event):
		"""Opens the Queriet website"""
		os.startfile('https://github.com/oliver2213/queriet')

	def OpenIssuePage(self, event):
		"""Opens the github issues page"""
		os.startfile('https://github.com/oliver2213/queriet/issues')
	def AddPluginsToList(self):
		"""This method adds each plugin found in self.controller.plugins to lists that need them, currently only the main listbox.
			This method gets run each time the plugins list is rebuilt."""
		self.log.debug("Adding plugins to the UI list...")
		if self.apiList.IsEmpty()==False:
			self.log.debug("Plugin list already has items, clearing.")
			self.apiList.Clear()
		try:
			for plugin_info, plugin_object in self.controller.plugins.iteritems():
				self.apiList.Append(plugin_info.name, plugin_object)
		except:
			self.log.exception("Error adding plugin to list!")
		self.log.debug("Done!")

	def OnListChange(self, event):
		sel = self.apiList.GetSelection()
		if sel < 0:
			return
		self.log.debug("API list selection changed.\n%s is now selected." %(sel))
		self.SetFocus(sel)

	def OnAbout(self, event):
		dlg = wx.MessageDialog(self, """Queriet, the quick ubiquitous extensible research interface enhancement tool, version %s. \nAuthors: %s. \nQueriet is a tool designed to give you quick access to information. With an open framework for developers to define plugins and all sourcecode freely available on Git Hub, we want to make it as easy as possible for anyone with a bit of programming knowledge to make plugins for queriet. \nEach plugin allows Queriet to get information from different sources. For more info, select the 'open website' item from the help menu.""" %(info.version, info.authors), "About Queriet")
		dlg.ShowModal()

	def OnClose(self, event):
		"""Delete system tray icon and this window."""
		self.log.debug("Closing UI...")
		try:
			self.icon.Destroy()
			self.Destroy()
		except:
			self.log.exception("Error closing UI!")

class SystemTrayIcon(wx.TaskBarIcon):
	"""Class that implements a system tray icon for Queriet"""

	def __init__(self, UI, text):
		"""This is the initialization for the system tray icon class. It creates the menus for use in CreatePopupMenu, and PopupMenu. It also gets passed the MainUI object so it can call it's methods for menu items."""
		super(SystemTrayIcon, self).__init__()
		self.log = logging.getLogger('Queriet.'+__name__)
		self.MUI = UI
		self.SetIcon(wx.NullIcon, text)
		self.CreateMenu()
		self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

	def CreateMenu(self):
		#Create our menu now, so we can reuse it later
		self.log.debug("Creating system tray menu...")
		try:
			self.menu = wx.Menu()
			self.showhide_item = utils.CreateMenuItem(self.menu, '&show or hide Queriet', self.MUI.showhide)
			self.openSite_item = utils.CreateMenuItem(self.menu, 'Open the Queriet &website', self.MUI.OpenSite)
			self.about = utils.CreateMenuItem(self.menu, 'About...', self.MUI.OnAbout, id=wx.ID_ABOUT)
			self.menu.AppendSeparator()
			self.exit_item = utils.CreateMenuItem(self.menu, 'e&xit', self.MUI.controller.OnClose, id=wx.ID_EXIT)
		except:
			self.log.debug("Done!")

	def CreatePopupMenu(self):
		"""Show the menu."""
		self.log.debug("Pop up system tray menu.")
		self.PopupMenu(self.menu)

	def on_left_down(self, event):
		"""When the system tray icon is left clicked, show / hide the main interface"""
		self.MUI.showhide(None) # it expects to be passed an event object, so we use none

	def OnClose(self, event):
		self.log.debug("Closing Queriet from the system tray.")
		try:
			wx.CallAfter(self.MUI.controller.close) #Run the top-level close method instead of just the UI's one, so other resources can be released if needed
		except:
			self.log.exception("Error closing Queriet from system tray!")