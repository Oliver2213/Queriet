# The Queriet application specification
This is, in general, just a place for the developers of queriet to hash out what, exactly, the application "does", and how it does it. If there is a feature you'd like to see, a suggestion you'd like to make, or general feedback you'd like to contribute about this document, please file an [issue](https://github.com/oliver2213/queriet/issues) or a [pull request](https://github.com/Oliver2213/Queriet/pulls).

## General overview

Queriet (The quick extensible ubiquitous interface enhancement tool), is meant to provide quick access to online resources. Need to look something up on wikipedia quickly? Convert 30 US Dollars to Canadian currency without going to google? Want to look up what a word means iether with a dictionary or the community-powered urban dictionary? Queriet will have you covered. Once things are set up, Queriet will run in the background, waiting for your keypress that launches the interface. The interface will have a few main elements:
* A list of APIs to choose from. You'll find items such as Wikipedia, Urban Dictionary, Dictionary.com, etc here. What you choose in this list affects where your search gets it's results from.
* a search field where you can type your query and a search button. Plugins can define their own input panel, so for an API that might require extra information for a specific search, plugins can define items such as check boxes, buttons, radiobuttons, etc. An example of this might be a Github search api, with a search field and radiobuttons allowing you to search users, repositories, issues, etc.
* A read-only textfield with the results of your search. As with the input panel, plugins can define an output panel with user interface elements. This could allow for say, a list of results, instead of a large read-only text field.
* A menu bar with common items such as close to tray, exit, about, open website, etc.

The app also has a system tray icon that, when left-double clicked, shows or hides the interface, and a right click menu with items such as show/hide, check for updates, open the Queriet site, etc.

### Note

If you're a graphic designer or artist, we could really use an icon for Queriet! :p

## Low-level components

These are various low-level things that need to be in place for a v1.0 release

* Get a working user interface. API list, basic search box, search button, read-only results field - Done!
* Get a working tray icon. This is done, we have right-click menu support, left double-click show / hide functionality. Things I'd like to add here:
  * An item to check for updates (when implemented)
  * an item to show the config dialog (when implemented)
  * Get a graphical icon to use in the tray and for the Queriet logo in general
* An extensible plugin system. This means that a plugin for Queriet could do whatever it needs to do to get results of a query, from whatever site or service it supports. This could be anything from hashing a block of text / file, converting monitary values, solving math equations, getting results for the query from urban dictionary, whatever. Plugins should also be able to build their own input and output pannels, so that plugins with more suffisticated searching systems can define their own UI elements. An example of this might be a twitter plugin to search tweets, with an input box and a set of radiobuttons for users, tweets, hashtags, or trends. Such an example plugin would most likely want to override the default read-only output field, in favor of a list with the results. Plugins would have to import wx and build a pannel with sizers containing their controls, and then save the resulting pannels to something like self.InputPanel and self.Output panel. If the main UI notices that the currently selected API in the list has it's own input and output, it would use those pannels instead of the default ones. As for plugin systems, so far, the use of [Yapsy](http://yapsy.sourceforge.net/) has been suggested for our plugin system, and this is probably what I'll go for, as it does what we had planned anyways. Idealy though, I'd like to have a dialog that allows the installation, updating, and removal of plugins. A file format like .queriet-plugin would be nice, for quick installation of downloaded plugins. - Done! (Whew, that was long-winded). 
We have a basic plugin system using Yapsy in place, though it will most definitly be tweaked further. As it stands now, plugins can define their own panels, panels change based on the list item in focus, and we have "stock" panels that basic plugins can use if there developers don't feel like building UI components or the API or service doesn't need anything fancy. This, also, will almost certainly be tweaked and changed.
* Implement a config file system, probably configobj, for storing and retrieval of values. As of now, current speculation is that each plugin will get it's own "data directory", in an OS-appropriate location on the filesystem. This should allow plugins to store their configuration in whatever format they choose, while still having a place to store other files if needed. There will probably be methods in the inherited plugin class so each plugin can get it's location. (core has config already set up, not so for plugin config path method, yet).
* Create an options dialog
* Get keyboard hooks working, and create a dialog that allows the user to define his / her own bindings, probably a tab on said options dialog. - Done! (Keyhooks working, no dialog yet)
* create an update checking system bassed off of the Git Hub releases page for this project. E.G. Compare latest version to current number, if greater retrieve the correct asset's URL, download it, then pop up a balloon telling the user it's done. We'll be using pUpdater4pi](https://github.com/phfaist/updater4pyi).

## The plugin interface

We are using [Yapsy](http://yapsy.sourceforge.net/) for plugin management and discovery, and so far things seem to be going well. Plugins need to inherit from PluginHandler.Plugin, and redefine methods such as activate, deactivate, and setup.

### Methods all plugins will need to support

This is pretty solid now, and there are very few methods your plugin absolutely *has* to have. The current list:

* Activate and Deactivate - these methods will be called when a plugin is activated and deactivated respectively. Plugins should *not* define their UI elements here, but instead use 'setup'. Plugins are activated, then set up. This is where plugins might want to register with any online APIs they will need (obtaining OAuth tokens and storing them, etc).
* OnGainFocus and OnLoseFocus: each plugin needs these methods in the main class. If your plugin doesn't need to do anything when it gains focus (such as loading results from a news site, pulling up previous searches), you can safely ignore this method - it's inherited from PluginHandler.Plugin. The default implementation calls the panel level focus methods, which should *only do panel specific things*. When I say, "gains or loses focus", I don't mean in the wx widgits terminology - when these methods get called, the plugin in question has just had it's name selected in the main list control.
* Each plugin needs an 'InfoPanel' object. This needs to inherit from wx.Panel, and can optionally have children panels, such as an input and output. You can use the provided panels in [defaultPanels](https://github.com/Oliver2213/Queriet/blob/master/queriet/defaultPanels.py) if your doing something simple, or define your own. 
  * OnGainFocus and OnLoseFocus: If you need to do panel-specific things, such as clearing the results and the input field after a search (recommended), you need to super this - the default implementation hides the panel when it loses focus and shows it when it receives it. Your plugin **must** show and hide it's panels when it gains and loses focus, respectively. This is to keep the interface consistent. These methods get called from the plugin level OnGain / LoseFocus methods.

As stated above, all plugins will inherit from the PluginHandler class, which will have methods those plugins can redefine.

### Results format

Since plugins are essentially defining their own user interface panels or customizing default ones, there isn't a standardized results object. It is up to each plugin' developer to decide how their plugin will return results. This shouldn't be too dificult - if your plugin searches a site for words or phraises, like a dictionary, your probably going to want to put the results in a read-only text field with maybe a link to the source material. If your plugin could potentially return lots of results a user might want to scroll through, you might opt for a list, where clicking or pressing enter on an entry brings up more details about it.