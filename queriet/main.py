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

#First off, we need to know if we're frozen, to load the configspec from the bundle if necessary
if getattr( sys, 'frozen', False):
	frozen=True
else:
	frozen=False

if frozen==True:
	config = conf.GetConfig(sys._MEIPASS+'/Queriet.confspec', 'Queriet.conf')
else:
	config = conf.GetConfig(os.path.dirname(os.path.abspath(__file__))+'/Queriet.confspec', os.path.dirname(os.path.abspath(__file__))+'/Queriet.conf')

log = SetupLogging('Queriet', config['logging']['log_level'], config['logging']['format'])

log.info("Queriet, version %s starting up" %(info.version))

if frozen==True:
	log.info("Queriet is running from a compiled executable.")
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