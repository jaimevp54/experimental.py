import functools
import inspect
from experimental_config import ENABLED_EXPERIMENTS

class DisabledExperiment(Exception):
	pass

class MismatchingArguments(TypeError):
	pass

def volatile(experiment, safe=False):
	if not ENABLED_EXPERIMENTS:
		raise Exception("ENABLED EXPERIMENTS NOT DEFINED")

	def decorated(func, *args, **kwargs):
		def wrapper(*args, **kwargs):	
			same_number_of_arguments = bool( len(inspect.getargspec(func).args) == len(inspect.getargspec(experiment).args) ) # TODO(jaimevp54): Refactor this into a function. validate_number_of_arguments()?
			if not same_number_of_arguments:
				raise MismatchingArguments("Experimental and volatile functions must have the same number of arguments") # TODO(jaimevp54): Add number of arguments to error message
				
			if "*" not in ENABLED_EXPERIMENTS and experiment.__name__ not in ENABLED_EXPERIMENTS:
				return func(*args, **kwargs)
			else:
				print("Running '"+ func.__name__ + "' as experimental function '" + experiment.__name__ +"'.")
				try:
					return experiment(*args, **kwargs)
				except:
					if safe:
						print("WARNING: There was an error while executing '"+ experiment.__name__ + "' falling back to '" + func.__name__ +"'.")
						return func(*args, **kwargs)
					else:
						raise
		
		return wrapper

	return decorated


def experimental(identifier=None):
	def decorated(func, *args, **kwargs):
		_identifier = identifier or func.__name__
		@functools.wraps(func)
		def experiment(*args, **kwargs):
			if '*' not in ENABLED_EXPERIMENTS and _identifier not in ENABLED_EXPERIMENTS:
				raise DisabledExperiment("'"+func.__name__ + "' is  a experimental feature and it has not been enabled")
			return func(*args, **kwargs)
		
		return experiment
	return decorated
