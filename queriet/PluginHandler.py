#This is the API handler of Queriet
#Please see the license file in the main directory of this repository for licensing information

from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager

class Plugin(IPlugin):
	"""This class is a template for a plugin. 
		We use yapsy for plugin management, so you need a basic ini config file with a .queriet-plugin extention, looking something like:
		[Core]
		Name = the API plugin's name. Usually this can be set to the name of the service you want this to handle, such as "wikipedia"
		Module = your_plugin_filename_without_extentions. Usually something like, "Searches twitter for tweets with your searchterm in them", will suffice.
		[Documentation]
		Version = the version of your APIPlugin. Integers only, please.
		Author = Author(s) of your plugin. E.G. author = some dude <some-dude@dudes.net>, Some Girl <some-girl@girls.net>
		Website = http://example.com/your_plugin
		
		Your APIPlugin will also need to support the following methods:
		getResult(searchtext) - This is the main one. This needs to return a Queriet result object, or a list of them. Whatever your APIPlugin needs to do (Look something up online, calculate a math problem, compute a file hash), you need to kick it off and return it here. It generally needs to be fast, too. In future there will probably be a setting to have Queriet begin caching results for each api as soon as the go button is pressed.
		inputPanel - This is a method that will be passed the "infoPanel" as a parrent. It is expected that this is instantiated like, wx.Panel(infoPanel). You can use this to change input your plugin receives. Also, PLEASE USE SIZERS!
		outputPanel - same as input, but deals with displaying results of a search. Maybe you want a big text field, a picture and a text field, etc etc.
	"""

	def __init__():
		pass
	#Should be the same name as your module name
	name="no name"
	def activate():
		"""Your plugin should run any code necessary to get ready to deal with searches or other operations your plugins do. Bind hotkeys, authorize to an API, whatever."""
		pass

	def deactivate():
		"""Your plugin needs to release any resources it may have acquired, unbind any hotkeys, clear any caches, etc..."""
		pass

	#The input and output panels are None by default, redefine them in your plugin to have the main UI use them
	InputPanel=None
	OutputPanel=None

def GetPluginManager():
	"""Returns a plugin manager object, with Queriet-specific settings."""
	pm=PluginManager(directories_list=['plugins'], plugin_info_ext='queriet-plugin')
	return pm
