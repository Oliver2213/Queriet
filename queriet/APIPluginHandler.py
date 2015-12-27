#This is the API handler of Queriet
#Please see the license file in the main directory of this repository for licensing information

class APIPlugin(object):
	"""This class is a template for an API plugin. 
		In order for an APIPlugin to be valid, it must have all of these variables in a "manifest.json" file inside your plugin's directory.
		Name - the API plugin's name. Usually this can be set to the name of the service you want this to handle, such as "wikipedia"
		Summary - A quick summary of what your plugin does. Usually something like, "Searches twitter for tweets with your searchterm in them", will suffice.
		Version - the version of your APIPlugin. Integers only, please.
		Author - Author(s) of your plugin. E.G. author="some dude <some-dude@dudes.net>, Some Girl <some-girl@girls.net>"
		enabled - If this plugin should be included in the list of services in Queriet's list. This should *always* be set to true for plugins you are distributing, we'll probably add a dialog that lets users disable / enable different plugins somewhere down the road.
		requires - This should be a list of the python modules your plugin requires, use the same format as pip, e.g. requests>=2.0. If your APIPlugin doesn't have any "requirements", good for you, just leave the list empty. Currently, Queriet won't install these or do anything with them really, but at some point in the future it should. E.g. requires=['requests', 'tweepy', 'goodreads >=1.0']
		Your APIPlugin will also need to support the following methods:
		getResult(searchtext) - This is the main one. This needs to return a Queriet result object, or a list of them. Whatever your APIPlugin needs to do (Look something up online, calculate a math problem, compute a file hash), you need to kick it off and return it here. It generally needs to be fast, too. In future there will probably be a setting to have Queriet begin caching results for each api as soon as the go button is pressed.
		inputPanel - This is a method that will be passed the "infoPanel" as a parrent. It is expected that this is instantiated like, wx.Panel(infoPanel). You can use this to change input your plugin receives. Also, PLEASE USE SIZERS!
		outputPanel - same as input, but deals with displaying results of a search. Maybe you want a big text field, a picture and a text field, etc etc.

	"""

	def __init__(self):
		pass #for now

	def list():
		"""Method that scans for plugins and returns a list"""
		pass