NOTIMPLEMENTED = "Needs to be implemented"

class OperatorElement():	
	'''All operators use this as base.'''
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
		return self.duration

	def __hash__(self):
		return hash(self.name)

	def __eq__(self, other):
		return self.name == other.name

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

	def execute(self):
		# Find the distance between target center and the current position.
		self.duration = self.body_part.accept(self)

		return self.duration

	def visit_finger(self, finger):
		return finger.move(self.target)













