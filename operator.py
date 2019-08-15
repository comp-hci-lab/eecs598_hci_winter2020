from abc import ABCMeta, abstractmethod

NOTIMPLEMENTED = "Needs to be implemented"

class OperatorElement():
	#All operators use this as base
	__metaclass__ = ABCMeta
	
	def __init__(self):
		self.duration = 0

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
	def execute(self, eyes):
		eyes.send()


class Auditory(Perceptual):

	def __init__(self):
		pass

	'''Send information to auditory short term memory'''
	def execute(self):
		# ears.send()
		pass


class Haptic(Perceptual):

	def __init__(self):
		pass

	'''Send information to haptic short term memory'''
	def execute(self):
		pass


class Cognitive(OperatorElement):

	def __init__(self):
		# #Have access to LTM/STM
		# self.long_term_memory = LongTermMemory()
		# self.short_term_memory = ShortTermMemory()
		pass


	def accept(self, visitor):
		visitor.visitCognitive(self)

	'''Create and send motor operator'''
	def send(self):
		pass

	'''Receive Perceptual operator to be put into memory'''
	def receive(self, percept_operator):
		pass

	'''Send information to short term memory'''
	def execute(self, item, type):
		# '''Send to auditory STM'''
		# if type == 'a':

		# '''Send to visual STM'''
		# elif type == 'v':

		# '''send to haptic STM'''
		# elif type == 'h':

		pass
		# self.short_term_memory.addToMemory(item)
		
	'''Retrieve information from short term memory'''
	def retrieve(self):
		pass


class MotorOperator(OperatorElement):

	def __init__(self, body_part):
		super(MotorOperator, self).__init__()
		self.body_part = body_part

	# def accept(self, visitor):
	# 	visitor.visitMotor(self)

	'''Motor operators can be either move, grasp, press'''
	def execute(self):
		self.body_part.accept(self)

	def visitFinger(self):
		pass
	
	def visitEye(self):
		pass

class Move(MotorOperator):

	def __init__(self, body_part, new_location_x, new_location_y):
		super(Move, self).__init__(body_part)
		self.new_location_x = new_location_x
		self.new_location_y = new_location_y

	def visitFinger(self, finger):
		# A = ((finger.location_x - new_location_x)**2 + (finger.location_y - new_location_y)**2)**.5
		finger.move(self.new_location_x, self.new_location_y)
		#TODO Compute time taken

	def visitEye(self, eye):
		eye.move(self.new_location_x, self.new_location_y)
