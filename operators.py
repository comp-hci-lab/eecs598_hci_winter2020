NOTIMPLEMENTED = "Needs to be implemented"

class OperatorElement():	
	'''All operators use this as base.'''
	def __init__(self, name, body_part):
		'''
		Abstract class constructor that sets a unique name describing this operator, and initializes all of its parameters.

		'''
		self.name = name
		self.body_part = body_part
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

	def __init__(self, name, body_part):
		super(Perceptual, self).__init__(name, body_part)
		self.duration = 340
		
class Visual(Perceptual):

	def __init__(self, name, body_part):
		super(Visual, self).__init__(name, body_part)


class Encode(Visual):

	def __init__(self, name, body_part, target):
		super(Encode, self).__init__(name, body_part)
		self.target = target
		self.K = 0.4
		self.f =  1.53
		self.k = 0.006
		self.t_prep = 0.200
		self.initiate_saccade = False

	def execute(self):
		''' Executes encoding of a target, stores the target in the short term memory, and returns the duration  of the  operatoion. '''

		# Convert the gaze into a vector with root at (self.body_part.location_x, self.body_part.location_y, 0).
		current_x = self.body_part.fixation_x - self.body_part.location_x
		current_y = self.body_part.fixation_y - self.body_part.location_y
		current_z = self.body_part.distance

		# Convert the target gaze into a vector with root at (self.body_part.location_x, self.body_part.location_y, 0).
		target_x = self.target.location_x - self.body_part.location_x
		target_y = self.target.location_y - self.body_part.location_y
		target_z = self.body_part.distance

		dot_product =  current_x*target_x + current_y*target_y + current_z*target_z
		magnitude_current = math.sqrt(current_x**2 + current_y**2 + current_z**2)
		magnitude_target = math.sqrt(target_x**2 + target_y**2 + target_z**2)

		theta = dot_product/(magnitude_current * magnitude_target)

		epsilon = math.arccos(theta)
		
		self.duration = self.K*(-1*math.log(self.f,2.0))*math.exp(self.k*epsilon)

		if self.duration > self.t_prep:
			# It takes a long time to encode, so tell the system that we need to do a saccade to come closer to the target we are encoding.
			self.duration = self.t_prep
			self.initiate_saccade = True

		return self.duration


class Auditory(Perceptual):

	def __init__(self, name, body_part):
		super(Auditory, self).__init__(name, body_part)


class Haptic(Perceptual):

	def __init__(self, name, body_part):
		super(Haptic, self).__init__(name, body_part)


class Cognitive(OperatorElement):

	def __init__(self, name, body_part):
		super(Cognitive, self).__init__(name, body_part)
		self.duration = 50

	def visit_ltm(self, ltm):
		pass

	def visit_stm(self, stm):
		pass


class RetrieveTargetLocation(Cognitive):

	def __init__(self, name, body_part, symbol):
		super(RetrieveTargetLocation, self).__init__(name, body_part)
		self.symbol = symbol
		self.symbol_location = None

	def execute(self):
		self.duration = self.body_part.accept(self)

		return self.duration

	def visit_ltm(self, ltm):
		self.duration, self.symbol_location = ltm.get(self.symbol, self.start)

		return self.duration

	def visit_stm(self, stm):
		return stm.get(self.symbol)

class ActivateTargetLocation(Cognitive):

	def __init__(self, name, body_part, symbol, symbol_location):
		super(ActivateTargetLocation, self).__init__(name, body_part)
		self.symbol = symbol
		self.symbol_location = symbol_location

	def execute(self):
		self.duration = self.body_part.accept(self)

		return self.duration

	def visit_ltm(self, ltm):
		self.duration = ltm.put(self.symbol, self.symbol_location, self.start)

		return self.duration

	def visit_stm(self, stm):
		return stm.get(self.symbol)


class MotorOperator(OperatorElement):

	def __init__(self, name, body_part):
		super(MotorOperator, self).__init__(name)
		self.body_part = body_part

	def visit_finger(self, finger):
		pass

	def visit_eyes(self, eyes):
		pass

class Move(MotorOperator):

	def __init__(self, name, body_part, target):
		super(Move, self).__init__(name, body_part)
		self.target = target

	def execute(self):
		self.duration = self.body_part.accept(self)

		return self.duration

	def visit_finger(self, finger):
		return finger.move(self.target)


	def visit_eyes(self, eyes):
		return eyes.move(self.target)













