#The Queriet application specification
This is, in general, just a place for the developers of queriet to hash out what, exactly, the application "does", and how it does it. If there is a feature you'd like to see, a suggestion you'd like to make, or general feedback you'd like to contribute about this document, please file an [issue](https://github.com/oliver2213/queriet/issues) or a [pull request](https://github.com/Oliver2213/Queriet/pulls).

##General overview

Queriet (The quick extensible ubiquitous interface enhancement tool), is meant to provide quick access to online resources. Need to look something up on wikipedia quickly? Convert 30 US Dollars to Canadian currency without going to google? Want to look up what a word means iether with a dictionary or the community-powered urban dictionary? Queriet will have you covered. Once things are set up, Queriet will run in the background, waiting for your keypress that launches the interface. The interface will have a few main elements:
* A list of APIs to choose from. You'll find items such as Wikipedia, Urban Dictionary, Dictionary.com, etc here. What you choose in this list affects where your search gets it's results from.
* a search field where you can type your query and a search button. Eventually plugins will be able to define their own input panel, so for an API that might require extra information for a specific search, plugins can define items such as check boxes, buttons, radiobuttons, etc. An example of this might be a Github search api, with a search field and radiobuttons allowing you to search users, repositories, issues, etc.
* A read-only textfield with the results of your search. As with the input panel, plugins will be able to define an output panel with user interface elements. This could allow for say, a list of results, instead of a large read-only text field.
* A close button, to send the app to the background again.

The app also has a system tray icon that, when left-double clicked, shows or hides the interface, and a right click menu with items such as show/hide, check for updates, open the Queriet site, etc.

###Note

If your a graphic designer or artest, we could really use an icon for Queriet! :p

##Low-level components

These are various low-level things that need to be in place for a v1.0 release

* Get a working user interface. API list, basic search box, search button, read-only results field - Done!
* Get a working tray icon. This is partially done, we have a menu with 2 items, right-click menu support, left double-click show / hide functionality. Things I'd like to add here:
  * An item to check for updates (when implemented)
  * an item to show the config dialog (when implemented)
  * Get a graphical icon to use in the tray and for the Queriet logo in general
* An extensible plugin system. This means that a plugin for Queriet could do whatever it needs to do to get results of a query, from whatever site or service it supports. This could be anything from hashing a block of text / file, converting monitary values, solving math equations, getting results for the query from urban dictionary, whatever. Plugins should also be able to build their own input and output pannels, so that plugins with more suffisticated searching systems can define their own UI elements. An example of this might be a twitter plugin to search tweets, with an input box and a set of radiobuttons for users, tweets, hashtags, or trends. Such an example plugin would most likely want to override the default read-only output field, in favor of a list with the results. Plugins would have to import wx and build a pannel with sizers containing their controls, and then save the resulting pannels to something like self.InputPanel and self.Output panel. If the main UI notices that the currently selected API in the list has it's own input and output, it would use those pannels instead of the default ones. As for plugin systems, so far, the use of [Yapsy](http://yapsy.sourceforge.net/) has been suggested for our plugin system, and this is probably what I'll go for, as it does what we had planned anyways. Idealy though, I'd like to have a dialog that allows the installation, updating, and removal of plugins. A file format like .queriet-plugin would be nice, for quick installation of downloaded plugins. - Done! (Whew, that was long-winded). 
We have a basic plugin system using Yapsy in place, though it will most definitly be tweaked further. As it stands now, plugins can define their input and output panels, panels change based on the list item in focus, and we have "stock" panels that basic plugins can use if there developers don't feel like building UI components or the API or service doesn't need anything fancy. This, also, will almost certainly be tweaked and changed, and we still need to define a standard results object that (like the stock UI elements), is there if you don't feel like definig your own, but is definitly expandable.
* Implement a config file system, probably configobj, for storing and retrieval of values. As of now, current speculation is that each plugin will get it's own "data directory", in an OS-appropriate location on the filesystem. This should allow plugins to store their configuration in whatever format they choose, while still having a place to store other files if needed. There will probably be methods in the inherited plugin class so each plugin can get it's location.
* Create an options dialog
* Get keyboard hooks working, and create a dialog that allows the user to define his / her own bindings, probably a tab on said options dialog
* create an update checking system bassed off of the Git Hub releases page for this project. E.G. Compare latest version to current number, if greater retrieve the correct asset's URL, download it, then pop up a balloon telling the user it's done. If we're feeling lazy, use [this updater](http://hg.q-continuum.net/updater/)

##The plugin interface

We are using [Yapsy](http://yapsy.sourceforge.net/) for plugin management and discovery, and so far things seem to be going well. Plugins need to inherit from PluginHandler.Plugin, and redefine methods such as activate, deactivate, and setup.

###Methods all plugins will need to support

We're still hammering this out, but as it stands now, we think that plugins will need to support these methods (Plugins will inherit from the PluginHandler class):

* getResults - this will be the main method called with search parameters. For plugins using the basic UI layout, this will just be a text argument, holding the text from the search box. For more advanced plugins, `*args` and `**kwargs` will need to be passed to this method to handle dynamic interface elements. Whatever a plugin needs to do to return results, (request data from an API, compute a file hash, calculate an answer to a math problem), it needs to kick it off and end it here.
* Activate and Deactivate - these methods will be called when a plugin is activated and deactivated respectively. Plugins might want to build their UI elements here, ready for use when a search is performed. They also might want to register with any online APIs they will need (obtaining OAuth tokens and storing them, etc).
* inputPanel - If the plugin has more advanced options for searching with the APIs it supports, it should define this in it's main class so that the main UI will notice and add it when the plugin in question is selected. This UI element can provide items such as checkboxes, radiobuttons, comboboxes, text fields, all in the context of searching for something. For example, a plugin that quickly tells the user the hash of a file with many different hashing algorithms might have a text field for entering the path of a file, a browse button for easier file location, a combobox with the hashing algorithm the user would like to use, and a start button, rather than the simple input text box the stock interface uses.
* outputPanel - If the plugin has a need to display search results in a different manner than the standard read-only textbox, it can define those elements here. Keeping our hashing plugin example from above, it might not need to define an output panel, as the standard read-only box is enough to display it's information. But for, say, a twitter search plugin, which could return many many results (such as tweets, users, trends, hashtags), the plugin author might wish to show those items in a list for easier readability and scrolling.

As stated above, all plugins will inherit from the PluginHandler class, which will have methods those plugins can redefine.

###Results format

Each plugin, after performing it's search or other work, needs to return some sort of standardized object. I'm thinking something like calling an PluginResult class with things like text, URL, APIName for each result, maybe plugins could define their own format as long as they build user interface elements to handle it.