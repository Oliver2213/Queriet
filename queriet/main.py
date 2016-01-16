#Queriet main application file
#Please see the license file in the main directory for licensing information

import conf
import info
import logging
from utils import SetupLogging
import wx
from controller import Controller

config = conf.GetConfig('Queriet.confspec', 'Queriet.conf')
log = SetupLogging('Queriet', config['logging']['log_level'], config['logging']['format'])

log.debug("Queriet, version %s starting up" %(info.version))
log.debug("Obtaining WX app object for UI")
app = wx.App()
log.debug("Done")
log.debug("Instantiating main controller")
MainController = Controller(app, config)
log.debug("Done, starting main controller")
MainController.run()