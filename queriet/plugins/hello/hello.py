import wx
import PluginHandler

class hello(PluginHandler.Plugin):
	def __init__(self):
		super(hello, self).__init__()

	def setup(self):
		self.InfoPanel = HelloInput(self.controller.ui.panel)

class HelloInput(PluginHandler.PluginPanel):
	def __init__(self, parent):
		super(HelloInput, self).__init__(parent)
		helloButton = wx.Button(self, label="Hello World", size = (150, 30))
		helloText = wx.TextCtrl(self, -1, style=wx.TE_READONLY, size=(200, 50))
		box = wx.BoxSizer(wx.VERTICAL)
		box.Add(helloText, 3)
		box.Add(helloButton)
		self.SetSizer(box)
