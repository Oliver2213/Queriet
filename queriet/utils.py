#Utility functions for Queriet
#Please see the license file in the main directory of this repository for such information

import logging
import wx

def CreateMenuItem(menu, label, func,  position=-1):
	"""A quick function to add and bind a menu item.
		This can be used for menubars, system tray icons, etc.
		Just pass it the menu object in question, a label for your new option, it's position (-1 by default, which appends to end), and a funcion you'd like to bind it to.
		By default, this function appends your item to the end of the menu, so the order in which you add items by calling this function is important to how the menu looks.
		Also, remember you can denote a shortcut key with the and (&) sign before the letter in the label.
		Coppied and slightly modified from http://stackoverflow.com/questions/6389580/quick-and-easy-trayicon-with-python
	"""
	item = wx.MenuItem(menu, position, label)
	menu.Bind(wx.EVT_MENU, func, id=item.GetId())
	menu.AppendItem(item)
	return item

def SetupLogging(caller):
	"""This method should only be ran once, from main.py.
		After that, all modules simply need to:
		import logging,
		log = logging.getLogger(__main__)
		They will then be able to send messages and exception info as needed, to log.debug, log.info, log.warning, log.error, log.critical.
		Note: this function accepts the name of the caller as an arg, as for some reason it appears that, even if said caller imports this function specifically from utils, the __name__ attribute isn't that of the caller
	"""
	log = logging.getLogger(caller) # get a logging object named with the current module running this
	log.setLevel(logging.DEBUG)
	#Define a standard log output format
	LogFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
	#Our stream and file handlers
	ConsoleHandler = logging.StreamHandler()
	ConsoleHandler.setLevel(logging.DEBUG)
	ConsoleHandler.setFormatter(LogFormat)
	FileHandler = logging.FileHandler('Queriet.log')
	FileHandler.setLevel(logging.DEBUG)
	FileHandler.setFormatter(LogFormat)
	log.addHandler(ConsoleHandler)
	log.addHandler(FileHandler)
	#Return our log object to caller, so it can use it
	return log