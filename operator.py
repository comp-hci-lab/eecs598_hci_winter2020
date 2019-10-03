from abc import ABCMeta, abstractmethod

NOTIMPLEMENTED = "Needs to be implemented"

class OperatorElement():
	#All operators use this as base
	__metaclass__ = ABCMeta
	
	def __init__(self, name):
		'''
		Abstract class constructor that sets a unique name describing this operator, and initializes all of its parameters.

		'''

		self.name = name
		self.duration = 0
		self.start = 0
		self.end = 0

	def execute(self):
		'''
		Executes this operator and returns its duration.
		'''
		raise NotImplementedError(NOTIMPLEMENTED)


class Perceptual(OperatorElement):
	def __init__(self, name):
		super(Perceptual, self).__init__(name)
		
class Visual(Perceptual):

	def __init__(self, name):
		super(Visual, self).__init__(name)


class Auditory(Perceptual):

	def __init__(self, name):
		super(Auditory, self).__init__(name)


class Haptic(Perceptual):

	def __init__(self, name):
		super(Haptic, self).__init__(name)


class Cognitive(OperatorElement):

	def __init__(self, name):
		super(Cognitive, self).__init__(name)


class MotorOperator(OperatorElement):

	def __init__(self, name, body_part):
		super(MotorOperator, self).__init__(name)
		self.body_part = body_part

	def visit_finger(self, finger):
		pass

class Move(MotorOperator):

	def __init__(self, name, body_part, target):
		super(Move, self).__init__(name, body_part)
		self.target = target
		self.a = 185.65 #TODO: set Fitts' Law parameter a
		self.b = 14.12 #TODO: set Fitts' Law parameter b

	def execute():
		# Find the distance between target center and the current position.
		target_x = target.top_left_x + target.width/2
		target_y = target.top_left_y + target.height/2
		
		A = Math.distance(body_part.new_location_x, body_part.new_location_y, target_x, target_y)
		W = Math.min(target.width, target.height)

		self.duration = self.a + self.b*Math.log2(A/W+1) #TODO: calculate duration using Fitts' Law.
		
		self.body_part.accept(self)

		return self.duration


	def visit_finger(self, finger):
		finger.move(new_location_x, new_location_y)













