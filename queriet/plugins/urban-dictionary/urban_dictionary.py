#Urban dictionary plugin, part of Queriet

from DefaultPanels import StandardInputPanel, ReadOnlyOutputPanel
import urbandict
import PluginHandler
import wx

class urban_dictionary(PluginHandler.Plugin):
	"""Plugin for queriet that, (you guessed it), allows lookup of words and phraises on urban dictionary via the 'urbandict' python module"""
	def __init__(self):
		super(urban_dictionary, self).__init__()
		#We don't really need to do anything here, no api tokens required with this package

	def setup():
		"""This method just creates the main info panel for urban dict and saves it for the UI to use"""
		self.InfoPanel = UrbanDictInfoPanel(self.controller.ui.panel)


class UrbanDictPanel(PluginHandler.PluginPanel):
	"""Panel class that sets up this plugin's UI"""
	
	def __init__(self, parent):
		super(UrbanDictPanel, self).__init__(parent)
		self.InputPanel = StandardInputPanel(self, self.Search, InputFieldString='Urbandictionary Search')
		self.OutputPanel = ReadOnlyOutputPanel(self)

	def Search(self):
		"""Don't confuse this with the search function, outside this class.
		This is merely a proxy method that gets the return value from that function and sets the read only textfield with the result(s).
		"""		
		if self.OutputPanel.output.GetValue() is None:
			return #No text in the field
		else:
			res = Search(self.OutputPanel.output.GetValue())
			self.OutputPanel.output.SetValue(res)

def Search(text):
	"""This method returns results, concatonated as a string, from urban dictionary"""
	results = urbandict.define(text)
	#returns a list
	string = ""
	if len(results)==0:
		string = "No results found."
		return string
	else:
		if len(results)==1: word = 'result' else: word = 'results'
		string+="""%s %s found.""" %(len(results), word)
		for entry in results:
			#Must have word atribute
			string +='%s:\r\n' %(entry['word'])
			#Must have definition
			string+="""%s\r\n""" %(entry['def'])
			if entry['example']:
				string+="""Example: %s""" %(entry['example'])
		return string