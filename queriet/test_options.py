import wx
from conf import GetConfig
from options import Options

class MainFrame(wx.Frame):
	def __init__(self, parent, title):
		super(MainFrame, self).__init__(parent, title=title, size=(1000, 800))
		self.setup()
		self.Center()
		self.Show()

	def setup(self):
		panel = wx.Panel(self)
		button = wx.Button(panel, label="Show Dialog")
		button.Bind(wx.EVT_BUTTON, self.ShowDialog)

	def ShowDialog(self, e):
		config = GetConfig("queriet.confspec", "queriet.conf")
		options = Options(config)
		options.ShowModal()
		options.Destroy()

app = wx.App()
mf = MainFrame(None, "Options test")
app.MainLoop()