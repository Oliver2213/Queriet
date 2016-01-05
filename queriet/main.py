#Queriet main application file
#Please see the license file in the main directory for licensing information

__version__=0.1
__author__='Blake Oliver <oliver22213@me.com>, Bradley Renshaw <bradjrenshaw@gmail.com>'

import logging
import wx
from controller import Controller

log = logging.getLogger(__name__)
LogFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
ConsoleHandler = logging.StreamHandler()
ConsoleHandler.setLevel(logging.DEBUG)
ConsoleHandler.setFormatter(formatter)
FileHandler = logging.FileHandler('Queriet.log')
FileHandler.setLevel(logging.DEBUG)
FileHandler.setFormatter(LogFormat)
log.addHandler(ConsoleHandler)
log.addHandler(FileHandler)
app = wx.App()
MainController = Controller(app)
MainController.run()