#Utility functions for Queriet
#Please see the license file in the main directory of this repository for such information

import logging
import wx

def CreateMenuItem(menu, label, func, id=None, help ="", kind=wx.ITEM_NORMAL):
	"""A quick function to add and bind a menu item.
		The point of this is to provide a wrapper around WX and be called by the application with all the arguments it needs (and with defaults that you can just not worry about if you don't need them). It will also handle binding to a menu event.
		This can be used for menubars, system tray icons, etc.
		Necessary info is the menu object in question, a label for your new option, and a funcion you'd like to bind it to. You can also provide a help text, the kind, and an ID, if your making a stock item (about, exit, new), it's best to use those so they look native on every OS.
		Kind can be one of: 
			wx.ITEM_SEPARATOR - a line in the menu separating items
			wx.ITEM_NORMAL - a normal clickable menu item (this is what is used if you don't specify a kind)
			wx.ITEM_CHECK - a checkable menu item, use item.Check(True), or item.Check(False) to control this
			wx.ITEM_RADIO - (I think...), an item that is exclusively checked. (You have 5 items, you can only have one checked)
		By default, this function appends your item to the end of the menu, so the order in which you add items by calling this function is important to how the menu looks.
		Also, remember you can denote a shortcut key with the and (&) sign before the letter in the label.
		Coppied and slightly modified from http://stackoverflow.com/questions/6389580/quick-and-easy-trayicon-with-python
	"""
	if id is None: id = wx.ID_ANY
	item = wx.MenuItem(menu, id, label, help, kind)
	menu.Bind(wx.EVT_MENU, func, id=item.GetId())
	menu.AppendItem(item)
	return item

def SetupLogging(caller, level, format):
	"""This method should only be ran once, from main.py.
		After that, all modules simply need to:
		import logging,
		log = logging.getLogger(__name__)
		They will then be able to send messages and exception info as needed, to log.debug, log.info, log.warning, log.error, log.critical.
		Note: this function accepts the name of the caller as an arg, as for some reason it appears that, even if said caller imports this function specifically from utils, the __name__ attribute isn't that of the caller
	"""
	log = logging.getLogger(caller) # get a logging object named with the current module running this
	if level == "debug":
		log.setLevel(logging.DEBUG)
	elif level == "info":
		log.setLevel(logging.INFO)
	elif level == "warning":
		log.setLevel(logging.WARNING)
	elif level == "error":
		log.setLevel(logging.ERROR)
	elif level == "critical":
		log.setLevel(logging.CRITICAL)
	YapsyLog = logging.getLogger('yapsy')
	#Define a standard log output format from config
	LogFormat = logging.Formatter(format)
	#Our stream and file handlers
	ConsoleHandler = logging.StreamHandler()
	ConsoleHandler.setLevel(logging.DEBUG)
	ConsoleHandler.setFormatter(LogFormat)
	FileHandler = logging.FileHandler('Queriet.log')
	FileHandler.setLevel(logging.DEBUG)
	FileHandler.setFormatter(LogFormat)
	#log.addHandler(ConsoleHandler)
	log.addHandler(FileHandler)
	YapsyLog.addHandler(ConsoleHandler)
	YapsyLog.addHandler(FileHandler)
	#Return our log object to caller, so it can use it
	return log