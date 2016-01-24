import wx
import copy

class Options(wx.Dialog):
	def __init__(self,config, parent=None, title="Queriet options"):
		super(Options, self).__init__(parent=parent, title=title)
		self.original_config = config
		self.config = copy.copy(config)
		self.SetupUI()
		self.Center()

	def SetupUI(self):
		self.panel = wx.Panel(self)
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.OptionsNB = OptionsNotebook(self, self.config)
		self.ok = wx.Button(self.panel, id=wx.ID_OK)
		self.ok.Bind(wx.EVT_BUTTON, self.OnOk)
		self.cancel = wx.Button(self.panel, id=wx.ID_CANCEL)
		self.cancel.Bind(wx.EVT_BUTTON, self.CloseDialog)
		self.sizer.Add(self.OptionsNB, wx.EXPAND, 5)
		self.sizer.Add(self.ok, 0, wx.ALIGN_BOTTOM, 10)
		self.sizer.Add(self.cancel, 0, wx.ALIGN_BOTTOM, 10)
		#self.panel.SetSizerAndFit(self.Sizer)
		self.SetSizer(self.sizer)
		self.Fit()
		self.Layout()
		#self.Show()

	def OnOk(self, e):
		self.SaveConfig()
		#e.Skip()
		self.EndModal(wx.ID_OK)

	def CloseDialog(self, e):
		#self.panel.Destroy()
		#e.Skip()
		self.EndModal(wx.ID_CANCEL)

	def SaveConfig(self):
		self.original_config = self.config
		self.original_config.write()

class OptionsNotebook(wx.Notebook):
	def __init__(self, parent, config):
		super(OptionsNotebook, self).__init__(parent, id=wx.ID_ANY)
		self.config = config
		self.Setup()

	def Setup(self):
		self.general = GeneralPanel(self, self.config['general'])
		self.logging = LoggingPanel(self, self.config['logging'])
		self.AddPage(self.general, "General")
		self.AddPage(self.logging, "Logging")
		self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

	def OnPageChanged(self, e):
		self.Layout()


class OptionsPanel(wx.Panel):
	def __init__(self, parent, config):
		super(OptionsPanel, self).__init__(parent, id=wx.ID_ANY)
		self.config = config
		self.setup()

	def setup(self):
		pass

class GeneralPanel(OptionsPanel):
	def setup(self):
		"""Sets up the general tab panel. Currently, it consists of only boolean values, so a simple config dictionary iteration is all we need."""
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		count = 0 # To allow us to set focus to the first checkbox
		for k, v in self.config.iteritems():
			if isinstance(v, bool):
				checkbox = wx.CheckBox(self, label=k.replace("_", " "))
				checkbox.SetValue(v)
				checkbox.Bind(wx.EVT_CHECKBOX, self.toggle)
				self.sizer.Add(checkbox)
				count+=1
				if count==1:
					checkbox.SetFocus()
		self.SetSizerAndFit(self.sizer)

	def toggle(self, e):
		checkbox = e.GetEventObject()
		self.config[checkbox.Label.replace(" ", "_")] = checkbox.GetValue()

class LoggingPanel(OptionsPanel):
	def setup(self):
		self.sizer = wx.GridBagSizer(10, 10)
		LogLevels = ["debug", "info", "warning", "error", "critical"]
		LogLevelLabel = wx.StaticText(self, label = "Logging level")
		LogLevelListBox = wx.ListBox(self, choices=LogLevels)
		LogLevelListBox.SetSelection(LogLevels.index(self.config['log_level']))
		LogLevelListBox.Bind(wx.EVT_LISTBOX, self.OnListChange)
		self.FormatLabel = wx.StaticText(self, label="Logging format")
		self.FormatInput = wx.TextCtrl(self, value=self.config['format'])
		self.FormatInput.Bind(wx.EVT_TEXT, self.FormatChange)
		self.sizer.Add(LogLevelLabel, pos=(1, 1))
		self.sizer.Add(LogLevelListBox, pos=(1, 2), span=(3, 1))
		self.sizer.Add(self.FormatLabel, pos=(5, 1))
		self.sizer.Add(self.FormatInput, pos=(5, 2), span=(1, 3))
		self.SetSizerAndFit(self.sizer)

	def FormatChange(self, e):
		self.config['format'] = e.GetEventObject().GetValue()

	def OnListChange(self, e):
		l = e.GetEventObject()
		if l.GetSelection()>=0:
			self.config['log_level'] = l.GetString(l.GetSelection())