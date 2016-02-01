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
		self.keybindings = KeystrokeEditor(self, self.config['keybindings'])
		self.AddPage(self.general, "General")
		self.AddPage(self.logging, "Logging")
		self.AddPage(self.keybindings, "Keybindings")
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

class KeystrokeEditor(OptionsPanel):
	#helper functions
	def list_to_string(self, l):
		return "+".join(l)
	def string_to_list(self, string):
		return string.split("+")
	def pass_checklist(self, string):
		self.SetCheckboxes(self.string_to_list(string)[:-1])
		self.Letter.SetValue(self.string_to_list(string)[-1:][0])
	def SetCheckboxes(self, l):
		self.ControlCheckbox.SetValue(True if "control" in l else False)
		self.WinCheckbox.SetValue(True if "win" in l else False)
		self.ShiftCheckbox.SetValue(True if "shift" in l else False)
		self.AltCheckbox.SetValue(True if "alt" in l else False)
	def setup(self):
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.OptionsListbox = wx.ListBox(self, choices=[])
		self.OptionsListbox.Bind(wx.EVT_LISTBOX, self.on_change)
		self.sizer.Add(self.OptionsListbox)
		self.ControlCheckbox=wx.CheckBox(self, label="Control")
		self.WinCheckbox=wx.CheckBox(self, label="Windows")
		self.AltCheckbox=wx.CheckBox(self, label="Alt")
		self.ShiftCheckbox=wx.CheckBox(self, label="Shift")
		self.Letter = wx.TextCtrl(self, -1)
		self.brb = wx.Button(self)
		self.brb.Bind(wx.EVT_BUTTON, self.on_push_brb)
		self.sizer.Add(self.ControlCheckbox)
		self.sizer.Add(self.WinCheckbox)
		self.sizer.Add(self.AltCheckbox)
		self.sizer.Add(self.ShiftCheckbox)
		self.sizer.Add(self.Letter)
		#Same pattern from above code, but set checkboxes based on first value
		count=0
		for k, v in self.config.iteritems():
			self.OptionsListbox.Append(k)
			count += 1
			if count==1:
				self.pass_checklist(self.config[k])
	def on_change(self, e):
		self.pass_checklist(self.config[self.OptionsListbox.GetString(self.OptionsListbox.GetSelection())])
	def on_push_brb(self, e):
		l=[]
		if self.ControlCheckbox.GetValue():
			l.append("control")
		if self.AltCheckbox.GetValue():
			l.append("alt")
		if self.WinCheckbox.GetValue():
			l.append("win")
		if self.ShiftCheckbox.GetValue():
			l.append("shift")
		l.append(self.Letter.GetValue())
		f=self.list_to_string(l)
		self.config[self.OptionsListbox.GetString(self.OptionsListbox.GetSelection())]=f