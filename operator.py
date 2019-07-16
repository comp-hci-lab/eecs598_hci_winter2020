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

	def accept(self, visitor):
		visitor.visitMotor(self)

	'''Motor operators can be either move, grasp, press'''
	def execute(self, type, body_part, new_location_x, new_location_y):
		if body_part.device == "button" and type == 'press':
			'''Need to pass location of hand'''
			body_part.device.press()
		else if body_part.device == None and type == 'grasp' and (body_part.location_x == new_location_x and body_part.location_y == new_location_y):
			body_part.grasp(body_part.location_x, body_part.location_y)
		else if body_part.device == None and type == 'grasp' and (body_part.location_x != new_location_x or body_part.location_y != new_location_y):
			body_part.accept(new_location_x, new_location_y)
			body_part.grasp(body_part.location_x, body_part.location_y)
		else if type == 'move':
			body_part.accept(new_location_x, new_location_y)
			if body_part.device != None:
				body_part.device.move(body_part.location_x, body_part.location_y, new_location_x, new_location_y)




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

