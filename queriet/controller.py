#This is the main controler for Queriet
#For licensing info, please see the "license" file in the main directory of this repository
#This file handles overall Queriet operations

from ui import MainUI
import PluginHandler

class Controller(object):
	def __init__(self, application):
		"""This method initializes our plugin system, builds a dict of the discovered plugins, maps them to their objects, and setts up our UI"""
		self.application = application
		self.SetupPlugins()
		self.SetupUI()
		self.BuildPluginList()

	def SetupPlugins(self):
		"""Sets up our plugin manager and activates all found plugins"""
		self.pm = PluginHandler.GetPluginManager()
		self.pm.collectPlugins()
		for plugin in self.pm.getAllPlugins():
			self.pm.activatePluginByName(plugin.name)

	def BuildPluginList(self):
		"""Build, or (re)build, the list of currently activated plugins, and store them in the dict self.plugins, keyed by name."""
		if not pm:
			self.SetupPlugins()
		if self.pm: # we have a plugin manager object
			self.plugins={}
			for plugin in self.pm.getAllPlugins():
				self.plugins[plugin.name]=plugin.plugin_object
			if self.ui:
				self.ui.AddPluginsToList()

	def SetupUI(self):
		"""Create a frame for the main UI and link it to the controller."""
		self.ui = MainUI(self, None, "Queriet")

	def run(self):
		"""Begin the main application loop, if applicable."""
		if self.ui:
			self.application.MainLoop()

	def close(self):
		"""This method is meant to kick off the process of exiting Queriet. 
			All menu items, exit buttons, etc, should come here first to start a top-down exit"""
		if self.ui:
			self.ui.OnClose(None)

