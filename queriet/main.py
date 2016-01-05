#Queriet main application file
#Please see the license file in the main directory for licensing information

__version__=0.1
__author__='Blake Oliver <oliver22213@me.com>, Bradley Renshaw <bradjrenshaw@gmail.com>'

import logging
from utils import SetupLogging
import wx
from controller import Controller

log = SetupLogging(__name__)

log.debug("Queriet, version %s starting up" %(__version__))
log.debug("Obtaining WX app object for UI")
app = wx.App()
log.debug("Done")
log.debug("Instantiating main controller")
MainController = Controller(app)
log.debug("Done, starting main controller")
MainController.run()