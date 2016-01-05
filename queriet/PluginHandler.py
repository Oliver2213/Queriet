#This is the plugin handler of Queriet
#Please see the license file in the main directory of this repository for licensing information

import wx
import logging
from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager

log = logging.getLogger('Queriet.'+__name__)

class Plugin(IPlugin):
	"""This class is a template for a plugin. 
		We use yapsy for plugin management, so you need a basic ini config file with a .queriet-plugin extention, looking something like:
		[Core]
		Name = the API plugin's name. Usually this can be set to the name of the service you want this to handle, such as "wikipedia"
		Module = your_plugin_filename_without_extentions. Usually something like, "Searches twitter for tweets with your searchterm in them", will suffice.
		[Documentation]
		Version = the version of your plugin.
		Author = Author(s) of your plugin. E.G. author = some dude <some-dude@dudes.net>, Some Girl <some-girl@girls.net>
		Website = http://example.com/your_plugin
		
		Your APIPlugin will also need to support the following methods:
		getResult(searchtext) - This is the main one. This needs to return a Queriet result object, or a list of them. Whatever your APIPlugin needs to do (Look something up online, calculate a math problem, compute a file hash), you need to kick it off and return it here. It generally needs to be fast, too. In future there will probably be a setting to have Queriet begin caching results for each api as soon as the go button is pressed.
		inputPanel - This is a method that will be passed the "infoPanel" as a parrent. It is expected that this is instantiated like, wx.Panel(infoPanel). You can use this to change input your plugin receives. Also, PLEASE USE SIZERS!
		outputPanel - same as input, but deals with displaying results of a search. Maybe you want a big text field, a picture and a text field, etc etc.
	"""

	def __init__(self):
		self.InputPanel = None
		self.OutputPanel = None

	def SetController(self, controller):
		self.controller = controller

	def setup(self):
		"""This would be a good place to assign your InputPanel and OutputPanels, if your using either of these"""
		pass

	def activate(self):
		"""Your plugin should run any code necessary to get ready to deal with searches or other operations your plugins do. Bind hotkeys, authorize to an API, whatever."""
		pass

	def deactivate(self):
		"""Your plugin needs to release any resources it may have acquired, unbind any hotkeys, clear any caches, etc..."""
		pass

	def on_gain_focus(self):
		"""Unless there is something special that your plugin needs to do when it is selected in the API listbox in the user interface, you probably shouldn't mess with this method.
			If, however, your plugin needs to start pulling data from the web (maybe to display in a list for a "top news" plugin), you should do that here by using Super to get what is defined here (which is the code to run the OnGainFocus and OnLoseFocus methods for your input and output panels).
		"""
		if self.InputPanel:
			self.InputPanel.on_gain_focus()
		if self.OutputPanel:
			self.OutputPanel.on_gain_focus()

	def on_lose_focus(self):
		"""This method runs when your plugin loses it's selection in the main UI API listbox. If you have some data cached in memory, (say a previous search), you might wanna go ahead and write it to disk, close any Http / https sessions, that sort of thing.
			Your plugin should not, however, release any resources it might have acquired, such as keybindings, temporary API tokens, etc - losing listbox focus just means the user is using (or might use, since they selected) another API in the list. Use the Deactivate method to release resources.
			Remember to use Super to get the functionality defined here, which just calls the OnLoseFocus method of your panels.
		"""
		if self.InputPanel:
			self.InputPanel.on_lose_focus()
		if self.OutputPanel:
			self.OutputPanel.on_lose_focus()

	def Activate(self):
		pas

	def Deactivate(self):
		pass


class pluginPanel(wx.Panel):
	"""The template for a plugin panel.
	
	An input or output panel for a plugin must have the following:
	- An on_gain_focus and on_lose_focus method. These will instantiate and change whatever they need to for the panels when they gain and lose focus when plugins change, respectively."""

	def on_gain_focus(self):
		"""This method should do things that are *specific* to the panel when it gets focus. This might be loading up previous searches from a config file, setting controls to their last position, etc."""
		pass

	def on_lose_focus(self):
		"""Again, this method needs to do things that are *specific* to the panel - the plugin's OnGainFocus and OnLoseFocus methods will handle everything else."""
		pass

def GetPluginManager():
	"""Returns a plugin manager object, with Queriet-specific settings."""
	log.debug("Obtaining a plugin manager...")
	pm=PluginManager(directories_list=['plugins'], plugin_info_ext='queriet-plugin')
	log.debug("Done! Plugin manager at %s" %(pm))
	return pm
