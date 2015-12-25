#This is the API handler of Queriet
#Please see the license file in the main directory of this repository for licensing information

class APIPlugin:
	"""This class is a template for an API plugin. 
		In order for an APIPlugin to be valid, it must have all of these.
		Name - the API plugin's name. Usually this can be set to the name of the service you want this to handle, such as "wikipedia"
		Version - the version of your APIPlugin
		Author - Author(s) of your plugin
		enabled - If this plugin should be included in the list of services in Queriet's list. This should *always* be set to true for plugins you are distributing, we'll probably add a dialog that lets users disable / enable different plugins somewhere down the road.
		requires - This should be a list of the python modules your plugin requires, use the same format as pip, e.g. requests>=2.0. If your APIPlugin doesn't have any "requirements", good for you, just leave the list empty. Currently, Queriet won't install these or do anything with them really, but at some point in the future it should.
		Your APIPlugin will also need to support the following methods:
		getResult(searchtext): This is the main one. This needs to return a Queriet result object

	"""