import math

NOTIMPLEMENTED = "Needs to be implemented"

 # Total of all object counts.

class OperatorElement():	
	'''All operators use this as base.'''
	def __init__(self, name, body_part):
		'''
		Abstract class constructor that sets a unique name describing this operator, and initializes all of its parameters.

		'''
		self.name = name
		self.body_part = body_part
		self.duration = 0
		self.start_time = 0
		self.end_time = 0

	def execute(self):
		'''
		Executes this operator and returns its duration.
		'''

		return self.duration

	def __execute(self):
		''' Subclasses should implement this execution method to take advantage of the execution check. '''
		pass

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

	f_total = 1.0

	def __init__(self, name, body_part, target):
		super(Encode, self).__init__(name, body_part)
		self.target = target
		self.K = 0.4
		self.f = {} # Counts of object being encoded.
		self.k = 0.006
		self.t_prep = 200
		self.initiate_saccade = False

	def execute(self):
		''' Executes encoding of a target, stores the target in the short term memory, and returns the duration  of the  operatoion. '''

		# Convert the gaze into a vector with root at (self.body_part.location_x, self.body_part.location_y, 0).
		current_x = self.body_part.fixation_x - self.body_part.location_x
		current_y = self.body_part.fixation_y - self.body_part.location_y
		current_z = self.body_part.handler_distance

		# Convert the target gaze into a vector with root at (self.body_part.location_x, self.body_part.location_y, 0).
		target_x = self.target.top_left_x + self.target.width/2 - self.body_part.location_x
		target_y = self.target.top_left_y + self.target.height/2 - self.body_part.location_y
		target_z = self.body_part.handler_distance

		dot_product =  current_x*target_x + current_y*target_y + current_z*target_z
		magnitude_current = math.sqrt(current_x**2 + current_y**2 + current_z**2)
		magnitude_target = math.sqrt(target_x**2 + target_y**2 + target_z**2)

		theta = dot_product/(magnitude_current * magnitude_target)

		epsilon = math.acos(theta)

		self.f_total += 1.0

		if self.target.name not in self.f.keys():
			self.f[self.target.name] = 0.0

		self.f[self.target.name] = self.f[self.target.name] + 1.0

		frequency = self.f[self.target.name] / self.f_total
		
		self.duration = self.K*(-1*math.log(frequency))*math.exp(self.k*epsilon)

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

	def __init__(self, name, ltm, vstm, symbol,  timestamp_offset):
		super(RetrieveTargetLocation, self).__init__(name, ltm)
		self.symbol = symbol
		self.symbol_location = None
		self.vstm = vstm

		self.timestamp_offset = timestamp_offset

	def execute(self):
		# First check if it vstm.
		self.duration, self.symbol_location = self.vstm.accept(self)

		# If not then check LTM.
		if self.symbol_location is None:
			self.duration, self.symbol_location = self.body_part.accept(self)

		return self.duration

	def visit_ltm(self, ltm):
		self.duration, self.symbol_location = ltm.get(self.symbol, self.start_time + self.timestamp_offset)

		return (self.duration, self.symbol_location)

	def visit_stm(self, stm):
		self.duration, self.symbol_location = stm.get(self.symbol)

		return (self.duration, self.symbol_location)

class ActivateTargetLocation(Cognitive):

	def __init__(self, name, ltm, vstm, symbol, symbol_location, timestamp_offset):
		super(ActivateTargetLocation, self).__init__(name, ltm)
		self.symbol = symbol
		self.symbol_location = symbol_location
		self.vstm = vstm

		self.timestamp_offset = timestamp_offset

	def execute(self):
		self.duration = self.body_part.accept(self)
		self.duration += self.vstm.accept(self)

		return self.duration

	def visit_ltm(self, ltm):
		self.duration = ltm.put(self.symbol, self.symbol_location, self.start_time + self.timestamp_offset)

		return self.duration

	def visit_stm(self, stm):
		return stm.put(self.symbol, self.symbol_location)


class MotorOperator(OperatorElement):

	def __init__(self, name, body_part):
		super(MotorOperator, self).__init__(name, body_part)

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













