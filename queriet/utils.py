#Utility functions for Queriet
#Please see the license file in the main directory of this repository for such information

import wx
def CreateMenuItem(menu, label, func,  position=-1):
	"""A quick function to add and bind a menu item.
		This can be used for menubars, system tray icons, etc.
		Just pass it the menu object in question, a label for your new option, it's position (-1 by default, which appends to end), and a funcion you'd like to bind it to.
		By default, this function appends your item to the end of the menu, so the order in which you add items by calling this function is important to how the menu looks.
		Also, remember you can denote a shortcut key with the and (&) sign before the letter in the label.
		Coppied and slightly modiefied from http://stackoverflow.com/questions/6389580/quick-and-easy-trayicon-with-python
	"""
	item = wx.MenuItem(menu, position, label)
	menu.Bind(wx.EVT_MENU, func, id=item.GetId())
	menu.AppendItem(item)
	return item
