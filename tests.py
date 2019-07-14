import unittest
from experimental import volatile, experimental, DisabledExperiment, MismatchingArguments
from mock import patch
class TestVolatileDecorator(unittest.TestCase):
	def test_calls_enabled_experiment(self):
		@experimental()
		def e_func():
			return id(e_func)
			
		@volatile(experiment=e_func)
		def v_func():
			return id(v_func)
		
		with patch('experimental.ENABLED_EXPERIMENTS', []):
			self.assertEqual(id(v_func), v_func())

		with patch('experimental.ENABLED_EXPERIMENTS', ['other_func']):
			self.assertEqual(id(v_func), v_func())

		with patch('experimental.ENABLED_EXPERIMENTS', ['*']):
			self.assertEqual(id(e_func), v_func())

		with patch('experimental.ENABLED_EXPERIMENTS', ['e_func']):
			self.assertEqual(id(e_func), v_func())

	def test_different_number_of_arguments_raises_exception(self):
		@experimental()
		def e_func():
			return id(e_func)
			
		@volatile(experiment=e_func)
		def v_func(a):
			return id(v_func)
		
		with patch('experimental.ENABLED_EXPERIMENTS', ['*']):
			with self.assertRaises(MismatchingArguments):
				v_func("FAIL")

	def test_safe_flag(self):
		@experimental()
		def e_func():
			raise Exception
			return id(e_func)
			
		@volatile(experiment=e_func, safe=True)
		def v_func():
			return id(v_func)
		
		with patch('experimental.ENABLED_EXPERIMENTS', ['*']):
			self.assertEqual(id(v_func), v_func())

	def test_refactor_flag(self):
		
		ran_functions = []
		
		@experimental()
		def bad_refactor(original_list):
                    if original_list == [42] or original_list == None:
                        return list(original_list)
                    return original_list
			
		@volatile(experiment=bad_refactor, refactor=True)
                def get_same_list(original_list):
			return original_list
		
		with patch('experimental.ENABLED_EXPERIMENTS', ['*']):
                        a_list = []
			self.assertEqual(id(get_same_list(a_list)), id(a_list))
			
                        a_list = [42]
			self.assertNotEqual(id(get_same_list(a_list)), id(a_list))
			
			with self.assertRaises(Exception):
				get_same_list(None)
			
		with patch('experimental.ENABLED_EXPERIMENTS', []):
                        a_list = []
			self.assertEqual(id(get_same_list(a_list)), id(a_list))
			
                        a_list = [42]
			self.assertEqual(id(get_same_list(a_list)), id(a_list))

			

		

	
class TestExperimentalDecorator(unittest.TestCase):
	def test_experimental_function_raises_exception(self):
		@experimental()
		def func():
			pass

		with patch('experimental.ENABLED_EXPERIMENTS', []):
			with self.assertRaises(DisabledExperiment):
				func()

		with patch('experimental.ENABLED_EXPERIMENTS', ['otherFunction']):
			with self.assertRaises(DisabledExperiment):
				func()

		with patch('experimental.ENABLED_EXPERIMENTS', ['*']):
			try:
				func()
			except DisabledExperiment:
				self.fail("func() raised DisabledExperiment unexpectedly!")

		with patch('experimental.ENABLED_EXPERIMENTS', ['func']):
			try:
				func()
			except DisabledExperiment:
				self.fail("func() raised DisabledExperiment unexpectedly!")

	def test_identifier(self):
		@experimental('feature_A')
		def func():
			pass

		with patch('experimental.ENABLED_EXPERIMENTS', ['feature_A']):
			try:
				func()
			except DisabledExperiment:
				self.fail("func() raised DisabledExperiment unexpectedly!")

unittest.main()

# from experimental import experimental, volatile
# 
# 
# fruits = ["Banana", "Apple", "Strawberry"]
# 
# @experimental
# def print_fruits_twice(fruits):
# 	0/0
# 	print "This are my new fruits (printed twice ;D ) :"
# 	for fruit in fruits:
# 		print " - ", fruit, fruit
# 
# 
# @volatile(experiment=print_fruits_twice)
# def print_fruits(fruits):
# 	print "This are my new fruits:"
# 	for fruit in fruits:
# 		print " - ", fruit
# 
# 
# print_fruits(fruits)
# 
