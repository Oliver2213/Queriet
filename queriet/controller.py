#This is the main controler for Queriet
#For licensing info, please see the "license" file in the main directory of this repository
#This file handles overall Queriet operations

from ui import MainUI

class Controller(object):
	def __init__(self, application):
		self.application = application
		self.setup()

	def setup(self):
		"""Create a frame for the main UI and link it to the controller, as well as setting up a plugin handler."""
		self.ui = MainUI(self, None, "Queriet")

	def run(self):
		"""Begin the main application loop, if applicable."""
		if self.ui:
			self.application.MainLoop()

	def close(self):
		"""This method removes all necesary objects from memory."""
		if self.ui:
			self.ui.OnClose(None)

