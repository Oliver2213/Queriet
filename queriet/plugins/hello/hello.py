import wx
import PluginHandler
#import logging

class hello(PluginHandler.Plugin):
	def __init__():
		Super(hello, self).__init__()
		#self.log = logging.getLogger('Queriet.plugin'__class__)
		#print (__class__)

	def setup(self):
		self.log.debug("RUnning setup.")
		self.InputPanel = HelloInput(self.controller.ui.infoPanel)

	def Activate(self):
		self.log.debug("I'm activated!")

class HelloInput(PluginHandler.pluginPanel):
	def __init__(self, parent):
		super(HelloInput, self).__init__(parent)
		helloButton = wx.Button(self, label="Hello World", size = (150, 30))
		box = wx.BoxSizer(wx.VERTICAL)
		box.Add(helloButton)
		self.SetSizer(box)
