from PluginHandler import Plugin
import logging

class template(Plugin):
	def __init__(self):
		super(template, self).__init__()
		self.log = logging.getLogger('Queriet.plugin'+__name__)
		self.name = 'template'

	def Deactivate(self):
		self.log.debug("Template plugin deactivating.")