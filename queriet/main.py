#Queriet main application file
#Please see the license file in the main directory for licensing information

import conf
import os
import sys
import info
import logging
from utils import SetupLogging
import wx
from controller import Controller

config = conf.GetConfig('Queriet.confspec', os.path.dirname(os.path.abspath(__file__))+'/Queriet.conf')
log = SetupLogging('Queriet', config['logging']['log_level'], config['logging']['format'])

log.debug("Queriet, version %s starting up" %(info.version))
if getattr( sys, 'frozen', False ) :
	frozen=True
else:
	frozen=False
if frozen==True:
	log.debug("Queriet is running from a compiled executable.")
	log.debug("Changing directory to the temporary location where datafiles are... (%r)" %(sys._MEIPASS))
	try:
		os.chdir(sys._MEIPASS)
	except:
		log.error("Error while changing directory to %r!" %(sys._MEIPASS))

log.debug("Obtaining WX app object for UI...")
app = wx.App()
log.debug("Done!")
log.debug("Instantiating main controller...")
MainController = Controller(app, config)
log.debug("Done, starting main controller")
MainController.run()