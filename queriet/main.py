#Queriet main application file
#Please see the license file in the main directory for licensing information


import info
import logging
from utils import SetupLogging
import wx
from controller import Controller

log = SetupLogging('Queriet')

log.debug("Queriet, version %s starting up" %(info.version))
log.debug("Obtaining WX app object for UI")
app = wx.App()
log.debug("Done")
log.debug("Instantiating main controller")
MainController = Controller(app)
log.debug("Done, starting main controller")
MainController.run()