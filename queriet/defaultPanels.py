import wx
import PluginHandler

class inputPanel(PluginHandler.PluginPanel):
	"""Default input panel, used for inputting information for a query, can be API defined."""
	def __init__(self, parent):
		super(inputPanel, self).__init__(parent)
		self.inputStatic = wx.StaticText(self, -1, 'Search term or equation')
		self.input = wx.TextCtrl(self, -1)
		self.searchButton = wx.Button(self, -1, 'Search', size=(90, 30))
		self.inputSizer = wx.BoxSizer(wx.HORIZONTAL) # A sizer for items in the input panel
		self.inputSizer.Add(self.inputStatic, 1, wx.TOP|wx.LEFT|wx.BOTTOM, 5) # adding out input label
		self.inputSizer.Add(self.input, 3, wx.TOP|wx.BOTTOM, 10)
		self.inputSizer.Add(self.searchButton, 2, wx.TOP|wx.RIGHT|wx.BOTTOM, 20)
		self.SetSizer(self.inputSizer)
		self.Hide()

	def OnLoseFocus(self):
		self.input.Clear()

class outputPanel(PluginHandler.PluginPanel):
	"""The default output panel object, used to display the results of a query."""
	def __init__(self, parent):
		super(outputPanel, self).__init__(parent)
		self.outputSizer = wx.BoxSizer(wx.VERTICAL)
		self.outputStatic = wx.StaticText(self, -1, 'results', (5, 5))
		self.output = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.outputSizer.Add(self.outputStatic, 0, wx.TOP|wx.LEFT, 10)
		self.outputSizer.Add(self.output, 6, wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.EXPAND, 20)
		self.SetSizer(self.outputSizer)
		self.Hide()

	def ONLoseFocus(self):
		self.output.Clear()