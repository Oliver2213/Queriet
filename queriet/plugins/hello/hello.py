import wx
import PluginHandler

class hello(PluginHandler.Plugin):

	def setup(self):
		self.InputPanel = HelloInput(self.controller.ui.infoPanel)



class HelloInput(PluginHandler.pluginPanel):
	def __init__(self, parent):
		super(HelloInput, self).__init__(parent)
		helloButton = wx.Button(self, label="Hello World", size = (150, 30))
		box = wx.BoxSizer(wx.VERTICAL)
		box.Add(helloButton)
		self.SetSizer(box)
