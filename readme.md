# Queriet, the Quick ubiquitous extensible research interface enhancement tool

This project is in early beta, and it's purpose is to allow quick access to all kinds of information. The app runs quietly in the background, waiting for a key press that shows the interface, presenting you with the list of information sources and the associated UI controls for each (plugins can define their own UI elements). Speaking of plugins, it has a framework that allows anyone with a working knowledge of python to create them - the core deals with things like menu bar, system tray icon and menu, logging, config, keybindings, etc. All individual plugins need to do is define some metadata about themselves and create one panel with input and output controls. There are stock panels that can be instantiated with specific behaviors, so unless your doing something uncommon, that part is easy.
Editionally, plugins obviously need to deal with their own information backend, like a python API wrapper for their service, examples are Wikipedia, urban dictionary, etc.

## What we have so far

* An interface with a hotkey (windows q by default) that shows or hides the window. Within this window is a list of all the plugins that are installed, currently these include:
  * Dictionary with full definition, synonym, antonym, part of speech, example usage, hyphenation and pronunciation support.
  * urban Dictionary support

## We plan on adding the following soon:

  * Wikipedia
  * Wolfram alpha
  * Quick equation solving with sympy

As stated above, each plugin can define it's own UI elements, which allows for flexibility in how information is displayed. Dictionary definitions would most likely be in a text field, while, say, a twitter search would be in a list. Searches could also be narrowed or otherwise modified by checkboxes, radiobuttons, etc.


To view more on Queriet's progress, check out the [specification](/spec.md) or clone and check out the code. Pull requests and issue reports are welcome!.

## Requirements

To run Queriet from source, first, run pip -r requirements.txt in the main directory, then install the packages below:
* [WX Python](http://wxpython.org/) for the interface. This isn't in requirements.txt because, to my knowledge, it needs to be installed with a platform-specific binary package.
* [Vocabulary](https://pypi.python.org/pypi/Vocabulary/0.0.5) for the dictionary plugin. Just pip install vocabulary to get it.
* Specific plugins will probably define their own requirements, we'll most likely implement a system for downloading these as needed (plugin activation or plugin installation) for plugins that aren't in the official package.