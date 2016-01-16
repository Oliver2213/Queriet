import wx
import PluginHandler

#Some notes about these panels:
#They hide themselves by default, so if you are using them as children of your plugin's 'InfoPanel', make sure you 'Show' them, or pass autohide=False to their constructors.
#Also, they don't have OnGain / OnLoseFocus methods, these are building blocks and as such your plugin's focus methods are expected to clear the fields manually.


class StandardInputPanel(wx.Panel):
	"""Default input panel, used for inputting information for a query, can be API defined. 
		This panel is meant as a building block to be placed under an info panel which inherits from PluginHandler.PluginPanel, thus it does not need the OnGain / LoseFocus methods it's parent does.
	"""
	def __init__(self, parent, SearchFunc, InputFieldString='Search term or equation', SearchButtonString='Search', autohide=True, EnterFunc=None):
		"""
		Args:
			parrent: the wx window to set as this panel's parent. required
			SearchFunc: the function or method to bind to the search button. required
			InputFieldString: the text the input box should have. Defaults to "Search term or equation".	
			SearchButtonString: Text of the button. Defaults to "Search".
			autohide: If the input panel should automatically hide itself. Defaults to True.
			EnterFunc: Function to bind the enter key to, when pressed in the input field. Defaults to none. You can easily set this (for oneline input fields), to activate the search button by passing in the same function you passed to the 'SearchFunc' arg.
		"""
		super(StandardInputPanel, self).__init__(parent)
		self.inputStatic = wx.StaticText(self, -1, InputFieldString)
		if EnterFunc is not None:
			self.input = wx.TextCtrl(self, -1, style=wx.TE_PROCESS_ENTER)
			self.input.Bind(wx.EVT_TEXT_ENTER, EnterFunc)
		else:
			self.input = wx.TextCtrl(self, -1)
		self.SearchButton = wx.Button(self, -1, SearchButtonString)
		self.SearchButton.Bind(wx.EVT_BUTTON, SearchFunc)
		self.inputSizer = wx.BoxSizer(wx.HORIZONTAL) # A sizer for items in the input panel
		self.inputSizer.Add(self.inputStatic, 1, wx.TOP|wx.LEFT|wx.BOTTOM, 5) # adding our input label
		self.inputSizer.Add(self.input, 3, wx.TOP|wx.BOTTOM, 10)
		self.inputSizer.Add(self.SearchButton, 2, wx.TOP|wx.RIGHT|wx.BOTTOM, 20)
		self.SetSizer(self.inputSizer)
		if autohide == True:
			self.Hide()
		else:
			self.Show()


class ReadOnlyOutputPanel(wx.Panel):
	"""The default output panel object, used to display the results of a query.
		This panel is meant as a building block to be placed under an info panel which inherits from PluginHandler.PluginPanel, thus it does not need the OnGain / LoseFocus methods it's parent does.
	"""
	def __init__(self, parent, autohide=True):
		super(ReadOnlyOutputPanel, self).__init__(parent)
		self.outputSizer = wx.BoxSizer(wx.VERTICAL)
		self.outputStatic = wx.StaticText(self, -1, 'results', (5, 5))
		self.output = wx.TextCtrl(self, -1, size=(500, 500), style=wx.TE_MULTILINE|wx.TE_READONLY)
		#self.output.SetSize(self.output.GetBestSize())
		self.outputSizer.Add(self.outputStatic, 0, 10)
		self.outputSizer.Add(self.output, 3, wx.EXPAND|wx.ALL, 20)
		self.SetSizer(self.outputSizer)
		if autohide == True:
			self.Hide()
		else:
			self.Show()
