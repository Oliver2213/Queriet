# Queriet, the Quick ubiquitous extensible research interface enhancement tool
This project is in *extreme* alpha, but as it stands now, planned features are:

* quick access (via a global hotkey), to a dialog that allows you to search and display results for your term via the following sites (this list is subject to change):
  * Wikipedia
  * dictionary.com or another reputable online dictionary service
  * urbandictionary.com
  * Wolfram alpha
* Quick equation solving with sympy

All results will be displayed in the queriet window, with links to external sources for the respective service or site, if applicable.

To view more on Queriet's progress, check out the [specification](/spec.md).

## Requirements

To run Queriet from source, you'll need the following dependencies installed:
* [WX Python](http://wxpython.org/) for the interface.
* [Yapsy](http://yapsy.sourceforge.net/) for plugin installation, management, and removal.
* [Requests](https://github.com/kennethreitz/requests) for http communication, most, if not all, stock plugins will probably use this, other contributed plugins (if we get any once the project works correctly) might want to use requests for easing of specific http implementation, and in general it's a good package to have around.
* [ConfigObj](https://pypi.python.org/pypi/configobj/) and [validate](https://pypi.python.org/pypi/validate) for configuration file and specification loading, manipulating, and validation.
* [Vocabulary](https://pypi.python.org/pypi/Vocabulary/0.0.5) for the dictionary plugin.
* Specific plugins will probably define their own requirements, we'll most likely implement a system for downloading these as needed (plugin activation or plugin installation) for plugins that aren't in the official package.