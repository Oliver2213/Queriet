# This is the plugin handler of Queriet
# Please see the license file in the main directory of this repository for
# licensing information

import wx
import logging
from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager

log = logging.getLogger('Queriet.' + __name__)


class Plugin(IPlugin):
    """This class is a template for a plugin.
            We use yapsy for plugin management, so you need a basic ini config file with a .queriet-plugin extention, looking something like:
            [Core]
            Name = the API plugin's name. Usually this can be set to the name of the service you want this to handle, such as "wikipedia"
            Module = your_plugin_filename_without_extentions. Usually something like, "Searches twitter for tweets with your searchterm in them", will suffice.
            [Documentation]
            Version = the version of your plugin.
            Author = Author(s) of your plugin. E.G. author = some dude <some-dude@dudes.net>, Some Girl <some-girl@girls.net>
            Website = http://example.com/your_plugin

            Your APIPlugin will also need to support the following methods:
            getResult(searchtext) - This is the main one. This needs to return a Queriet result object, or a list of them. Whatever your APIPlugin needs to do (Look something up online, calculate a math problem, compute a file hash), you need to kick it off and return it here. It generally needs to be fast, too. In future there will probably be a setting to have Queriet begin caching results for each api as soon as the go button is pressed.
            inputPanel - This is a method that will be passed the "infoPanel" as a parrent. It is expected that this is instantiated like, wx.Panel(infoPanel). You can use this to change input your plugin receives. Also, PLEASE USE SIZERS!
            outputPanel - same as input, but deals with displaying results of a search. Maybe you want a big text field, a picture and a text field, etc etc.
    """

    def __init__(self):
        """Method that initializes a plugin, but does not 'activate'
                Make sure you 'super' this method, as it also gets a logging object, so you can use like
                        self.log.debug('test")
                later on in your plugin."""
        self.InfoPanel = None

    def SetController(self, controller):
        """Best not to redefine this, it runs when the plugin is passed a pointer to the main controller, saving it to self.controller.
                It also creates local pointers to RegisterKey, and UnRegisterKey so plugins can create keybindings to functions.
                Note that any functions that will be called by a hotkey need to have an "event" argument, and can't take any others.
        """
        self.controller = controller
        self.RegisterKey = self.controller.RegisterKey
        self.UnregisterKey = self.controller.UnRegisterKey

    def setup(self):
        """This would be a good place to assign your info panel, if your using either of these"""
        pass

    def Activate(self):
        """Your plugin should run any code necessary to get ready to deal with searches or other operations your plugins do. Bind hotkeys, authorize to an API, whatever."""
        pass

    def Deactivate(self):
        """Your plugin needs to release any resources it may have acquired, unbind any hotkeys, clear any caches, etc..."""
        pass

    def OnGainFocus(self):
        """Unless there is something special that your plugin needs to do when it is selected in the API listbox in the user interface, you probably shouldn't mess with this method.
                If, however, your plugin needs to start pulling data from the web (maybe to display in a list for a "top news" plugin), you should do that here by using Super to get what is defined here (which is the code to run the OnGainFocus and OnLoseFocus methods for your input and output panels).
        """
        self.InfoPanel.OnGainFocus()

    def OnLoseFocus(self):
        """This method runs when your plugin loses it's selection in the main UI API listbox. If you have some data cached in memory, (say a previous search), you might wanna go ahead and write it to disk, close any Http / https sessions, that sort of thing.
                Your plugin should not, however, release any resources it might have acquired, such as keybindings, temporary API tokens, etc - losing listbox focus just means the user is using (or might use, since they selected) another API in the list. Use the Deactivate method to release resources.
                Remember to use Super to get the functionality defined here, which just calls the OnLoseFocus method of your panels.
        """
        self.InfoPanel.OnLoseFocus()


class PluginPanel(wx.Panel):
    """The template for a plugin panel.

    Currently, an input or output panel for a plugin must have the following:
            OnGainFocus and OnLoseFocus methods which will (by default), show and hide their panels, respectively. If you need these methods to do something *UI specific*, then redefine and super or show and hide manuall.
            Your methods *MUST* show and hide when gaining or losing focus!
    """

    def OnGainFocus(self):
        """This method should do things that are *specific* to the panel when it gets focus. This might be loading up previous searches from a config file, setting controls to their last position, etc. It must always show the panel."""
        self.Show()

    def OnLoseFocus(self):
        """Again, this method needs to do things that are *specific* to the panel - the plugin's OnGainFocus and OnLoseFocus methods will handle everything else. THis method must always hide it's panel."""
        self.Hide()


def GetPluginManager():
    """Returns a plugin manager object, with Queriet-specific settings."""
    log.debug("Obtaining a plugin manager...")
    pm = PluginManager(directories_list=[
                       'plugins'], plugin_info_ext='queriet-plugin')
    log.debug("Done! Plugin manager at %s" % (pm))
    return pm
