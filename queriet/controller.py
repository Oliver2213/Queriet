#This is the main controler for Queriet
#For licensing info, please see the "license" file in the main directory of this repository
#This file handles overall Queriet operations

from ui import MainUI
import PluginHandler

class Controller(object):
	def __init__(self, application):
		"""This method initializes our plugin system, builds a dict of the discovered plugins, maps them to their objects, and setts up our UI"""
		self.application = application
		self.SetupPlugins() # Get a plugin manager object and activate all found plugins
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
		if not self.pm:
			self.SetupPlugins()
		if self.pm: # we have a plugin manager object
			self.plugins={}
			for plugin in self.pm.getAllPlugins():
				self.plugins[plugin.name]=plugin.plugin_object
				plugin.plugin_object.SetController(self)
				plugin.plugin_object.setup()
			if self.ui:
				self.ui.AddPluginsToList()

	def SetupUI(self):
		"""Create a frame for the main UI and link it to the controller."""
		self.ui = MainUI(self, None, "Queriet")

	def ShutDownPlugins(self):
		"""This method goes through and calls the Deactivate method of each plugin.
			This allows them to *properly* release any resources they have, stop any threads, close any sockets, write and close to any files, etc."""
		for plugin in self.plugins:
			plugin.Deactivate()

	def run(self):
		"""Begin the main application loop, if applicable."""
		if self.ui:
			self.application.MainLoop()

	def close(self):
		"""This method is meant to kick off the process of exiting Queriet. 
			All menu items, exit buttons, etc, should come here first to start a top-down exit"""
		if self.ui:
			self.ui.OnClose(None)
		self.ShutdownPlugins()

