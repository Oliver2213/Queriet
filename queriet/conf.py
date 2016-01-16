#Queriet config module

#We don't need both modules, just a few things from each
from configobj import ConfigObj, ParseError
from validate import Validator, ValidateError


#Our catch-all ConfError exception class

class ConfError(Exception): pass

def GetConfig(specpath, configpath):
	"""This function loads a config (if found), checks it against the provided specification, and returns it"""
	#Try to load the provided specification
	try:
		spec = ConfigObj(specpath, encoding='UTF8', list_values=False, interpolation=False, _inspec=True)
	except (ParseError, IOError) as e:
		raise ConfError("Error loading specification %r: %r" %(specpath, e))
	#Try to load the config
	try:
		config = ConfigObj(configpath, configspec=spec, create_empty=True, interpolation=False, encoding='UTF8')
	except ParseError as e: #No IOError because if we don't find the config file, we just create it from the spec
		raiseConfError("Error when loading config %r" %(configpath))
	#Now validate it...
	val = Validator()
	valid = config.validate(val, copy=True)
	if valid == True:
		#Config is valid, write it back to disk to make sure it has all values specified in the spec
		config.write()
	#return the config to caller
	return config