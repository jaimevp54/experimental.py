import functools
import inspect
import wrapt

from experimental_config import ENABLED_EXPERIMENTS

class DisabledExperiment(Exception):
	pass

class MismatchingArguments(TypeError):
	pass

def volatile(experiment, safe=False, refactor=False):
	if not ENABLED_EXPERIMENTS:
		raise Exception("ENABLED EXPERIMENTS NOT DEFINED")
        @wrapt.decorator
	def wrapper(subject, instance, args, kwargs):
			subject_arguments_count = len(inspect.getargspec(subject).args)
			experiment_arguments_count = len(inspect.getargspec(experiment).args)
			if subject_arguments_count != experiment_arguments_count:
				raise MismatchingArguments(
					"Subjects and experiments must have the same number of arguments. '{}' has {} arguments while '{}' has {}.".format(
						subject.__name__,
						subject_arguments_count,
						experiment.__name__,
						experiment_arguments_count
					)
				) # TODO(jaimevp54): Add number of arguments to error message
				
			if "*" not in ENABLED_EXPERIMENTS and experiment.__name__ not in ENABLED_EXPERIMENTS:
				return subject(*args, **kwargs)
			else:
				#print("Running '"+ subject.__name__ + "' as experimental function '" + experiment.__name__ +"'.")
				try:
					experiment_result = experiment(*args, **kwargs)
					subject_result = subject(*args, **kwargs)
					if refactor and experiment_result != subject_result:
						return subject_result
					return experiment_result
					
				except:
					if safe:
						#print("WARNING: There was an error while executing '"+ experiment.__name__ + "' falling back to '" + func.__name__ +"'.")
						return subject(*args, **kwargs)
					else:
						raise
	return wrapper

def experimental(identifier=None):
        @wrapt.decorator
	def wrapper(experiment, instance, args, kwargs):
		_identifier = identifier or experiment.__name__
                if '*' not in ENABLED_EXPERIMENTS and _identifier not in ENABLED_EXPERIMENTS:
                        raise DisabledExperiment("'"+experiment.__name__ + "' is  a experimental feature and it has not been enabled")
                return experiment(*args, **kwargs)
	return wrapper
