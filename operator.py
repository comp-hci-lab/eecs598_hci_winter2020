from abc import ABCMeta, abstractmethod

NOTIMPLEMENTED = "Needs to be implemented"

class OperatorElement():
	#All operators use this as base
	__metaclass__ = ABCMeta
	
	def __init__(self):
		pass

	@abstractmethod
	def accept(self, visitor):
		raise NotImplementedError(NOTIMPLEMENTED)

	#Return a set of properties for what happens when you execute it (Time, cycle, etc)
	#should return a snapshot of what is going on at that time along with how long it took
	def execute(self):
		raise NotImplementedError(NOTIMPLEMENTED)


class Perceptual(OperatorElement):

	def __init__(self, storage):
		#Initialize Perceptual values
		#Need access to some sort of some storage
		self.storage = storage

	def accept(self, visitor):
		visitor.visitPerceptual(self)
		
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


class Cognitive(OperatorElement):

	def __init__(self):
		#Have access to LTM/STM
		self.long_term_memory = LongTermMemory()
		self.short_term_memory = ShortTermMemory()


	def accept(self, visitor):
		visitor.visitCognitive(self)


	'''Send information to short term memory'''
	def execute(self):
		pass
		
	'''Retrieve information from short term memory'''
	def retrieve(self):
		pass


class Motor(OperatorElement):

	def __init__(self):
		pass

	def accept(self, visitor):
		visitor.visitMotor(self)

	'''Make it so the correct action is taken based on the device held (i.e. button = push, key = press, NO_ITEM = grasp)'''
	def execute(self, device):
		if device.type == "button":
			'''Need to pass location of hand'''
			device.press()



class Operator(OperatorElement):
	def __init__(self):
		self.elements = [Perceptual(), Cognitive(), Motor()]

	def accept(self, visitor):
		for element in self.elements:
			element.accept(visitor)

	def execute(self):
		pass

class OperatorElementVisitor():
	__metaclass__ = ABCMeta
	@abstractmethod
	def visitPerceptual(self, element):
		raise NotImplementedError(NOTIMPLEMENTED)

	@abstractmethod
	def visitCognitive(self, element):
		raise NotImplementedError(NOTIMPLEMENTED)

	@abstractmethod
	def visitMotor(self, element):
		raise NotImplementedError(NOTIMPLEMENTED)


class OperatorElementDoVisitor(OperatorElementVisitor):
	def visitPerceptual(self, perceptual):
		pass

	def visitCognitive(self, cognitive):
		pass

	def visitMotor(self, motor):
		pass

