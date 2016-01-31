#Queriet user interface file
#Please see the license file in the main directory for licensing information

import logging
import os
import wx
import utils
import info
from options import Options

class MainUI(wx.Frame):
	"""Class that holds the main user interface for Queriet"""
	def __init__(self, controller, parent, title):
		super(MainUI, self).__init__(parent, title=title, size=(1000, 800))
		self.log = logging.getLogger('Queriet.'+__name__)
		self.log.info("User interface starting up.")
		self.controller = controller
		self.setup()
		self.SetupMenuBar()
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.CreateIcon()
		self.Center()
		if self.controller.config['general']['open_interface_on_startup'] == True:
			self.Show()
		else:
			self.icon.ShowBalloon("Queriet running!", "Queriet is now running in the background, awaiting your use.", 3000)

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
		self.ListSizer.Clear()

		self.ListSizer.Add(self.apiStatic, 1, wx.EXPAND) # adding this label to our api sizer
		self.ListSizer.Add(self.apiList, 3, wx.EXPAND) #Add it to the list sizer
		self.ListSizer.Layout()
		self.ListPanel.SetSizer(self.ListSizer)
		self.ListPanel.Fit()
		self.MainSizer.Add(self.ListPanel, 1)
		if self.InfoPanel:
			self.MainSizer.Add(self.InfoPanel, 3, wx.EXPAND)
		self.MainSizer.Layout()
		self.panel.SetSizer(self.MainSizer)
		self.panel.Fit()


	def SetupMenuBar(self):
		"""Setup our menubar.
			Menu bar menus as well as items should be named like: self.MenuBar_file (the file, menu), self.MenuBar_file_exit (an exit item in the file menu)
		"""
		self.log.debug("Setting up menu bar...")
		try:
			self.MenuBar = wx.MenuBar()
			self.MenuBar_file = wx.Menu()
			self.MenuBar_file_options = utils.CreateMenuItem(self.MenuBar_file, "&Options...", self.ShowOptions)
			self.MenuBar_file_hide = utils.CreateMenuItem(self.MenuBar_file, 'Close to &tray', self.showhide)
			self.MenuBar_file_exit = utils.CreateMenuItem(self.MenuBar_file, 'E&xit', self.controller.Close, id=wx.ID_EXIT)
			
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

	def ChangeFocus(self, value):
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

	def ShowOptions(self, e):
		"""Display the options dialog"""
		self.log.debug("Getting options dialog.")
		DLG = Options(self.controller.config, parent=None, title="Queriet options")
		self.log.debug("Showing options dialog.")
		res = DLG.ShowModal()
		self.log.debug("Options dialog returned with value %s." %(res))
		DLG.Destroy()

	def showhide(self, event=None):
		"""This method shows or hides the main UI, depending on it's current state. It gets called by the main hotkey, the "OnClose" method (if that's the choice the user wants), and the system tray "show / hide" menu item"""
		if self.Shown:
			self.Hide()
			self.log.debug("Window hidden.")
		else:
			self.Show()
			self.apiList.SetFocus()
			self.log.debug("Window shown and set focus.")

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
		"""Event handler for the plugin / API listbox. This gets called when the focus of the aforementioned list changes and notifies the selected plugin that it now has focus and can show it's UI panel and run GetFocus related code."""
		sel = self.apiList.GetSelection()
		if sel < 0:
			return
		self.log.debug("Plugin / API list selection changed.\n%s is now selected." %(sel))
		self.ChangeFocus(sel)

	def OnAbout(self, event):
		"""Displays the standard "about" dialog that gives information on the program."""
		dlg = wx.MessageDialog(self, """Queriet, the quick ubiquitous extensible research interface enhancement tool, version %s. \nAuthors: %s. \nQueriet is a tool designed to give you quick access to information. With an open framework for developers to define plugins and all sourcecode freely available on Git Hub, we want to make it as easy as possible for anyone with a bit of programming knowledge to make plugins for queriet. \nEach plugin allows Queriet to get information from different sources. For more info, select the 'open website' item from the help menu.""" %(info.version, info.authors), "About Queriet")
		dlg.ShowModal()
		dlg.Destroy()

	def OnClose(self, event):
		"""This method performs the "correct" action to close Queriet.
			Note that this event handler catches the "close" method (generated when the user clicks the x in the title bar), and does *not* perform an actual exit.
			This means when a user uses a command like alt f4 or clicks the "close" button in the main UI, Queriet runs this method which, depending on their preffrences, will either hide to the task bar icon (recommended), or actually exit.
		"""
		self.log.debug("User clicked close in main UI.")
		if self.controller.config['dialogs']['exit_action'] == False: # We haven't asked the user what they want to do yet, let's do so
			self.log.debug("The user hasn't been asked about exiting to the background. Asking now...")
			dlg = wx.MessageDialog(self, "Queriet needs to run in the background to be available quickly for information lookup. When you exit the main window, the application would like to keep running in the background, waiting for you when you need it, even when the interface is hidden. Queriet is very light on system resources, and you can change this later in settings. Do you want to close to tray (recommended)?", "Keep running in background?", style=wx.YES_NO|wx.CANCEL|wx.ICON_QUESTION)
			res = dlg.ShowModal()
			self.log.debug("User said yes, run in the background: %s. User canceled close: %s." %(res==wx.ID_YES, res==wx.ID_CANCEL))
			dlg.Destroy()
			if res == wx.ID_YES:
				self.controller.config['dialogs']['exit_action'] = True
				self.controller.config['general']['exit_to_tray'] = True
			elif res == wx.ID_NO:
				self.controller.config['dialogs']['exit_action']=True
				self.controller.config['general']['exit_to_tray'] = False
			elif res == wx.ID_CANCEL: #You scared em off!
				return
		if self.controller.config['general']['exit_to_tray'] == True:
			self.log.debug("Exited to tray")
			self.showhide(None)
		elif self.controller.config['general']['exit_to_tray'] == False: #bale out!
			self.log.debug("Exit to tray disabled, starting a top-down exit.")
			self.controller.Close(None)

	def DoClose(self, event):
		"""Delete system tray icon and this window. Do not confuse it with the "OnClose" method, which performs an action based on what the user has set in config - this is when you really want to close, it should be run in a top-down manner (from controller), from which all good exiting starts."""
		self.log.debug("Closing UI...")
		try:
			self.icon.Destroy()
			wx.GetApp().ExitMainLoop()
		except:
			self.log.exception("Error closing UI!")

class SystemTrayIcon(wx.TaskBarIcon):
	"""Class that implements a system tray icon for Queriet"""
	def __init__(self, UI, text):
		"""This is the initialization for the system tray icon class. It creates the menus for use in 'CreatePopupMenu'. It also gets passed the MainUI object so it can call it's methods for menu items."""
		super(SystemTrayIcon, self).__init__()
		self.log = logging.getLogger('Queriet.'+__name__)
		self.MUI = UI
		self.SetIcon(wx.NullIcon, text)
		self.CreateMenu()
		self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

	def CreateMenu(self):
		"""Creates a reusable menu for the tray icon"""
		self.log.debug("Creating system tray menu...")
		try:
			self.menu = wx.Menu()
			self.showhide_item = utils.CreateMenuItem(self.menu, '&show or hide Queriet', self.MUI.showhide)
			self.openSite_item = utils.CreateMenuItem(self.menu, 'Open the Queriet &website', self.MUI.OpenSite)
			self.options_item = utils.CreateMenuItem(self.menu, '&Options...', self.MUI.ShowOptions)
			self.about = utils.CreateMenuItem(self.menu, 'About...', self.MUI.OnAbout, id=wx.ID_ABOUT)
			self.menu.AppendSeparator()
			self.exit_item = utils.CreateMenuItem(self.menu, 'e&xit', self.MUI.controller.Close, id=wx.ID_EXIT)
			self.log.debug("Done!")
		except:
			self.log.error("Error creating menu!")

	def CreatePopupMenu(self):
		"""Show the menu."""
		self.log.debug("Pop up system tray menu.")
		self.PopupMenu(self.menu)

	def on_left_down(self, event):
		"""When the system tray icon is left clicked, show / hide the main interface"""
		self.MUI.showhide(None) # it expects to be passed an event object, so we use none
