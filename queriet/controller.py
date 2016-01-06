#This is the main controler for Queriet
#For licensing info, please see the "license" file in the main directory of this repository
#This file handles overall Queriet operations

from ui import MainUI
import PluginHandler
import logging

class Controller(object):
	def __init__(self, application):
		"""This method gets a logging object, initializes our plugin system, builds a dict of the discovered plugins, maps them to their objects, and setts up our UI"""
		self.log = logging.getLogger('Queriet.'+__name__)
		self.log.debug("Starting initialization.")
		self.application = application
		self.SetupPlugins() # Get a plugin manager object and activate all found plugins
		self.SetupUI()
		self.BuildPluginList()
		self.log.info("Controller initialized.")

	def SetupPlugins(self):
		"""Sets up our plugin manager and activates all found plugins"""
		self.log.debug("Setting up plugins...")
		self.pm = PluginHandler.GetPluginManager()
		self.pm.collectPlugins()
		self.log.debug("Activating collected plugins.")
		for plugin in self.pm.getAllPlugins():
			self.log.debug("Activating plugin %s, version %s, by %s" %(plugin.name, plugin.version, plugin.author))
			try:
				self.pm.activatePluginByName(plugin.name)
			except:
				logging.exception("Loading plugin '%s' failed!" %(plugin))

	def BuildPluginList(self):
		"""Build, or (re)build, the list of currently activated plugins, and store them in the dict self.plugins, keyed by name."""
		self.log.debug("Building the list of available plugins...")
		if not self.pm:
			self.log.warning("Tried to build a list of plugins, but no plugin manager object found, obtaining one.")
			self.SetupPlugins()
		if self.pm: # we have a plugin manager object
			self.plugins={}
			for plugin in self.pm.getAllPlugins():
				#The plugins dict is keyed by the plugin's info object, with the value being the instantiated plugin
				#This, however, is just an abstraction over the yapsy layer. We can use the iteration "plugin" object, which is really a yapsy info object, to get variable plugin info, like name, author, version, etc
				self.plugins[plugin]=plugin.plugin_object
				self.log.debug("Added plugin %s " %(plugin.name))
				try:
					plugin.plugin_object.SetController(self)
				except: 
					self.log.exception("Unable to pass a controller instance to plugin '%s'" %(plugin.name))
				try:
					plugin.plugin_object.setup()
				except:
					self.log.exception("Error when setting up plugin '%s'" %(plugin.name))
			self.log.debug("%d total plugins added to plugins dictionary." %(len(self.plugins)))
			if self.ui:
				self.ui.AddPluginsToList()
			else:
				self.log.warning("Built plugins list, but no UI object was found, so not adding them to the UI listbox.")

	def SetupUI(self):
		"""Create a frame for the main UI and link it to the controller."""
		try:
			self.ui = MainUI(self, None, "Queriet")
		except:
			self.log.exception("Error creating main interface!")

	def ShutdownPlugins(self):
		"""This method goes through and calls the Deactivate method of each plugin.
			This allows them to *properly* release any resources they have, stop any threads, close any sockets, write and close to any files, etc."""
		#We need both the plugin_info and plugin_object, to make logging calls 
		for plugin_info, plugin_object in self.plugins.iteritems():
			try:
				self.log.debug("Deactivating plugin '%s'" %(plugin_info.name))
				plugin_object.Deactivate()
			except:
				self.log.exception("Error deactivating plugin '%s'" %(plugin_info.name))

	def run(self):
		"""Begin the main application loop, if applicable."""
		if self.ui:
			self.log.debug("Started main app loop.")
			self.application.MainLoop()
		else:
			self.log.error("No user interface found, can not start app main loop!")

	def OnClose(self, event):
		"""This method is meant to kick off the process of exiting Queriet. 
			All menu items, exit buttons, etc, should come here first to start a top-down exit"""
		self.log.info("Queriet starting shutdown.")
		if self.ui:
			self.log.debug("Closing UI.")
			self.ui.OnClose(None)
		if self.pm:
			self.log.debug("Deactivating all plugins.")
			self.ShutdownPlugins()

