#Queriet config module

import configobj
import validate

def GetConfig(specpath, configpath):
	"""This function loads a config (if found), checks it against the provided specification, and returns it"""
	#Load the provided specification
	spec = configobj.ConfigObj(specpath, encoding='UTF8', list_values=False, _inspec=True)
	#Load the config
	config = configobj.ConfigObj(configpath, configspec=spec, create_empty=True, encoding='UTF8')
	#Now validate it...
	val = validator.Validator()
	valid = config.validate(val, copy=True)
	if valid == True:
		#Config is valid, write it back to disk to make sure it has all values specified in the spec
		config.write()
	#return the config to caller
	return config