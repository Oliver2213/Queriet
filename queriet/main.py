#Queriet main application launch file
#Please see the license file in the main directory for licensing information


import wx
from controller import Controller

app = wx.App()
MainController = Controller(app)
MainController.run()