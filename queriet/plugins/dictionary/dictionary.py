#Dictionary plugin for Queriet
#For licensing information, see Queriet's license in the main directory

import json
import PluginHandler
import wx
import defaultPanels
from vocabulary import Vocabulary as voc

class DictionaryPlugin(PluginHandler.Plugin):
	"""Plugin that provides normal dictionary services for Queriet, uses the python 'vocabulary' module."""
	def __init__(self):
		#Not much to do here, just super and do what Plugin does
		super(DictionaryPlugin, self).__init__()

	def setup(self):
		"""Obtain the panel for this plugin so core can use it."""
		self.InfoPanel = DictionaryInfoPanel(self.controller.ui.panel)

	def OnLoseFocus(self):
		"""Clear the controlls"""
		self.InputPanel.input.Clear()
		self.InputPanel.Radiobox.SetSelection(0)
		self.OutputPanel.output.Clear()


class DictionaryInfoPanel(PluginHandler.PluginPanel):
	"""Main panel for the dictionary plugin"""
	def __init__(self, parent):
		super(DictionaryInfoPanel, self).__init__(parent)
		self.choices=['definition', 'synonym', 'antonym', 'part of speech', 'example usage', 'pronunciation', 'hyphenation']
		self.choicedict = {self.choices[0] : defin, self.choices[1] : syno, self.choices[2] : anton, self.choices[3] : partos, self.choices[4] : usagex, self.choices[5] : pronun, self.choices[6] : hyphen}
		self.InputPanel = defaultPanels.InputPanelWithRadiobox(self, self.Search, self.choices, InputFieldString='Dictionary lookup', EnterFunc=self.Search, autohide=False)
		self.OutputPanel = defaultPanels.ReadOnlyOutputPanel(self, autohide=False)
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.InputPanel, 1)
		self.sizer.Add(self.OutputPanel, 4)
		self.sizer.Layout()
		self.SetSizer(self.sizer)
		self.Fit()
		self.Hide()

	def Search(self, event):
		"""Search for the word provided, with the method selected."""
		if self.InputPanel.input.GetValue()==None or self.InputPanel.input.GetValue() == "":
			return # No text in the field, do nothing.
		val = self.InputPanel.Radiobox.GetSelection()
		txt = self.InputPanel.input.GetValue()
		result = GetResultString(self.choicedict[self.choices[val]], txt)
		self.OutputPanel.output.SetValue(result)


#Functions to return stringified representations of 'vocabulary' results
def GetResultString(vtype, term):
	"""
		Return a flat text string of the type specified.
		The methods 'meaning', 'usage_example',  and 'synonym' return lists of dicts, the returned format has 2 keys: text, and seq (sequence number). The format is json, which gets converted to python datatypes by this function.
		The 'antonym' method returns a python dictionary, with a list as the 'text' attribute, each entry in the list has an antonym
		The 'part_of_speech' method returns normal json, as a list. It follows the standard "2-key" format that meaning and synonym do, but adding an 'example' key as well. This also gets converted to a normal python dictionary.
	"""
	res = vtype['func'](term)
	if res == False:
		return "No results."
	if vtype['is_json']:
		res = json.loads(res)
	string = ""
	if len(res)==0: #No results
		return "No results."
	word = 'result' if len(res) ==1 else 'results'
	string += "%d %s:\n" %(len(res), word)
	if isinstance(vtype['returntype'], list):
		for item in res:
			if vtype['name'] == 'definition' or vtype['name'] == 'synonym' or vtype['name'] == 'usage example': #All of these use the same general format
				string += '%d, %s\n' %(item['seq']+1, item['text'])
			elif vtype['name'] == 'part of speech':
				string += '%d, %s\nExample: %s\n' %(int(item['seq']+1), item['text'], item['example:'])
			elif vtype['name'] == 'pronunciation':
				string += '%d, %s.\n' %(int(item['seq']+1), item['raw'])
			elif vtype['name'] == 'hyphenation':
				if item['seq'] == len(item['text']): #we've reached the end of the word,
					end='\n'
				else:
					end = ' '
				if 'type' in item.keys():
					string += '%s (%s)%s' %(item['text'], item['type'], end)
				else: #No type for this word piece
					string += '%s%s' %(item['text'], end)
	elif isinstance(vtype['returntype'], dict):
		if vtype['name'] == 'antonym':
			#only one attribute in the return dict if we are looking for antonyms, the text attribute is a list of them though
			count=0
			for item in res['text']:
				string += '%d, %s.\n' %(int(count+1), item)
				count+=1
	return string


#constants

defin={
	'name' : 'definition',
	'func' : voc.meaning,
	'is_json' : True,
	'returntype' : list()
}

syno = {
	'name' : 'synonym',
	'func' : voc.synonym,
	'is_json' : True,
	'returntype' : list()
}

anton = {
	'name' : 'antonym',
	'func' : voc.antonym,
	'is_json' : False,
	'returntype' : dict()
}

partos = {
	'name' : 'part of speech',
	'func' : voc.part_of_speech,
	'is_json' : True,
	'returntype' : list()
}

usagex = {
	'name' : 'usage example',
	'func' : voc.usage_example,
	'is_json' : True,
	'returntype' : list()
}

pronun = {
	'name' : 'pronunciation',
	'func' : voc.pronunciation,
	'is_json' : False,
	'returntype' : list()
}

hyphen = {
	'name' : 'hyphenation',
	'func' : voc.hyphenation,
	'is_json' : True,
	'returntype' : list()
}