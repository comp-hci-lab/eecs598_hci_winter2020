class Operator():
	#All operators use this as base
	def __init__(self):
		pass

	def execute(self):
		#Return a set of properties for what happens when you execute it (Time, cycle, etc)
		#should return a snapshot of what is going on at that time along with how long it took


class Perceptual(Operator):

	def __init__(self, storage):
		#Initialize Perceptual values
		#Need access to some sort of some storage
		self.storage = storage
		
class Visual(Perceptual):

	def __init__(self):
		pass

	'''Send information to visual short term memory'''
	def execute(self):
		pass


class Auditory(Perceptual):

	def __init__(self):
		pass

	'''Send information to auditory short term memory'''
	def execute(self):
		pass


class Haptic(Perceptual):

	def __init__(self):
		pass

	'''Send information to haptic short term memory'''
	def execute(self):
		pass


class Cognitive(Operator):

	def __init__(self):
		#Have access to LTM/STM
		self.long_term_memory = LongTermMemory()
		self.short_term_memory = ShortTermMemory()

	'''Send information to short term memory'''
	def execute(self):
		pass
		
	'''Retrieve information from short term memory'''
	def retrieve(self):
		pass


class Motor(Operator):

	def __init__(self):
		pass

	def execute(self):
		pass
