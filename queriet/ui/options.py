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

	def OnOk(self, e):
		self.SaveConfig()
		self.EndModal(wx.ID_OK)

	def CloseDialog(self, e):
		#self.panel.Destroy()
		self.EndModal(wx.ID_CANCEL)

	def SaveConfig(self):
		self.original_config = self.config
		self.original_config.write()

class OptionsNotebook(wx.Notebook):
	"""The main notebook that holds the entire options dialog and it's pages"""

	def __init__(self, parent, config):
		super(OptionsNotebook, self).__init__(parent, id=wx.ID_ANY)
		self.config = config
		self.Setup()

	def Setup(self):
		"""Sets up the options dialog and initializes each page"""
		self.general = GeneralPanel(self, self.config['general'])
		self.logging = LoggingPanel(self, self.config['logging'])
		self.keybindings = KeybindingEditor(self, self.config['keybindings'])
		self.AddPage(self.general, "General")
		self.AddPage(self.logging, "Logging")
		self.AddPage(self.keybindings, "Keybindings")
		self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

	def OnPageChanged(self, e):
		self.Layout()


class OptionsPanel(wx.Panel):
	"""A class that should be inherited by all classes that are notebook page objects"""
	def __init__(self, parent, config):
		super(OptionsPanel, self).__init__(parent, id=wx.ID_ANY)
		self.config = config
		self.setup()

	def setup(self):
		pass


class GeneralPanel(OptionsPanel):
	"""The general tab panel"""

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
		"""Method that changes a config value relating to a specific checkbox. We need this because we don't explicitly name each one, and who wants to have specific handlers? That's just lame."""
		checkbox = e.GetEventObject()
		self.config[checkbox.Label.replace(" ", "_")] = checkbox.GetValue()


class LoggingPanel(OptionsPanel):
	"""Logging tab panel"""

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


class KeybindingEditor(OptionsPanel):
	"""Tab in the options dialog that allows updating of keybindings""" 

	#helper functions

	def list_to_string(self, l):
		"""Converts a list like:
			['control', 'win', 'alt', 'space']
			To:
			control+win+alt+space
		"""
		return "+".join(l)

	def string_to_list(self, string):
		"""This splits a string like:
			"control+win+alt+space"
			To:
			['control', 'win', 'alt', 'space]
		"""
		return string.split("+")

	def set_binding(self, string):
		"""Sets up the checkboxes and text field for one keybinding"""
		self.SetCheckboxes(self.string_to_list(string)[:-1])
		self.key.SetValue(self.string_to_list(string)[-1:][0])

	def SetCheckboxes(self, l):
		"""Sets 4 checkboxes: control, win, alt, and shift, based on a list passed.
			The list should look like: ['control', 'shift', 'a']
		"""
		self.ControlCheckbox.SetValue(True if "control" in l else False)
		self.WinCheckbox.SetValue(True if "win" in l else False)
		self.ShiftCheckbox.SetValue(True if "shift" in l else False)
		self.AltCheckbox.SetValue(True if "alt" in l else False)

	def setup(self):
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.OptionsListbox = wx.ListBox(self, choices=[])
		self.OptionsListbox.Bind(wx.EVT_LISTBOX, self.on_list_change)
		self.sizer.Add(self.OptionsListbox)
		self.ControlCheckbox=wx.CheckBox(self, label="Control")
		self.WinCheckbox=wx.CheckBox(self, label="Windows")
		self.AltCheckbox=wx.CheckBox(self, label="Alt")
		self.ShiftCheckbox=wx.CheckBox(self, label="Shift")
		self.key = wx.TextCtrl(self, -1)
		self.key.SetMaxLength(10)
		#Set event handlers for the checkboxes
		for item in [self.ControlCheckbox, self.WinCheckbox, self.AltCheckbox, self.ShiftCheckbox]:
			item.Bind(wx.EVT_CHECKBOX, self.on_binding_updated)
		#We have to bind the text field event separately because the event it emits (as well as the one we're looking for in the text field's case) is different from that of the checkbox
		self.key.Bind(wx.EVT_TEXT, self.on_binding_updated)
		#Add the modifier checkboxes and text field to the sizer
		self.sizer.Add(self.ControlCheckbox)
		self.sizer.Add(self.WinCheckbox)
		self.sizer.Add(self.AltCheckbox)
		self.sizer.Add(self.ShiftCheckbox)
		self.sizer.Add(self.key)
		#Same pattern from above code, but set checkboxes based on first value
		count=0
		for k, v in self.config.iteritems():
			self.OptionsListbox.Append(k)
			count += 1
			if count==1:
				self.OptionsListbox.SetSelection(0)
				self.set_binding(self.config[k])

	def on_list_change(self, e):
		"""The event handler for when the listbox (and the focused keybinding), changes."""
		self.set_binding(self.config[self.OptionsListbox.GetString(self.OptionsListbox.GetSelection())])

	def on_binding_updated(self, e):
		"""This method saves the currently focused binding back to config. It's called whenever any of the checkboxes are toggled or the text in the text field changes.
			Note that the actual program configuration hasn't yet been modified - only the local instance of it. It will become the new configuration only if the OK button is pressed.
		"""
		l=[]
		if self.ControlCheckbox.GetValue():
			l.append("control")
		if self.AltCheckbox.GetValue():
			l.append("alt")
		if self.WinCheckbox.GetValue():
			l.append("win")
		if self.ShiftCheckbox.GetValue():
			l.append("shift")
		l.append(self.key.GetValue())
		f=self.list_to_string(l)
		self.config[self.OptionsListbox.GetString(self.OptionsListbox.GetSelection())]=f
