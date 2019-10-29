from abc import ABC, ABCMeta, abstractmethod
from model_util	import Event, MoveBodyPartEvent
from operators import Perceptual, RetrieveTargetLocation, ActivateTargetLocation, Cognitive, MotorOperator, Move
import networkx as nx
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Human(): 
	''' This class represents a human with both cognition and body. In Assignment 2, this will be an abstraction where most complex aspects of the human will be removed, except body parts. '''
	def __init__(self, handler = None):
		self.body_parts = {}
		self.handler = handler

		# Controls how far random visual search jumps from current fixation.
		self.visual_search_sigma = 300

	def add_body_part(self, body_part):
		self.body_parts[body_part.name] = body_part

	def create_finger(self, name, location_x, location_y):
		'''  Creates and adds a new figure to  the human. '''
		finger = Finger(name, location_x, location_y, self.handler)
		self.add_body_part(finger)
		return finger

	def create_eyes(self, name, location_x, location_y, handler_distance):
		'''  Creates and adds a new figure to  the human. '''
		eyes = Eyes(name, location_x, location_y, handler_distance, self.handler)
		self.add_body_part(eyes)
		return eyes

	def create_ltm(self, name):
		'''  Creates and adds a new figure to  the human. '''
		ltm = LongTermMemory(name)
		self.add_body_part(ltm)

		return ltm

	def create_stm(self, name):
		'''  Creates and adds a new figure to  the human. '''
		stm = ShortTermMemory(name)
		self.add_body_part(stm)
		
		return stm

	def press(self, input):
		''' Instructs the human to press on a series of targets. The human implementation simulates and predict behavior and returns a resulting schedule chart. Clients can then evaluate the schedule chart for duration of operations.'''
		schedule_chart = nx.DiGraph()

		# TODO: Add operators to the graph. For each motor operator, find the key by using handler.find_descendant(), then move thumb to the position of the key in the  handler.

		operator_idx = 0
		previous_perceptual_operator = None
		previous_cognitive_operator = None
		previous_motor_finger_operator = None
		previous_motor_eyes_operator = None

		words = input.split(" ")

		word_count = 0

		for word in words:
			perceive_word = Perceptual(str(operator_idx) + '_perceptual:' + word, self.body_parts['eyes'])
			perceive_word.execute()
			schedule_chart.add_node(perceive_word)
			operator_idx += 1

			process_word = Cognitive(str(operator_idx) + '_cognitive:' + word, self.body_parts['vstm'])
			process_word.execute()
			schedule_chart.add_node(process_word)
			operator_idx += 1

			schedule_chart.add_edge(perceive_word, process_word)

			if word_count == 0:
				if previous_cognitive_operator is not None:
					schedule_chart.add_edge(previous_cognitive_operator, perceive_word)

			if previous_perceptual_operator is not None:
				schedule_chart.add_edge(previous_perceptual_operator, perceive_word)

			if previous_motor_operator is not None:
				schedule_chart.add_edge(previous_motor_operator, process_word)

			previous_motor_operator = None

			previous_cognitive_operator = process_word

			for character in (word + ' '):
				target = self.handler.find_descendant(character)

				# Locate target using LTM vs. visual search.

				# LTM
				retrieve_target_location = RetrieveTargetLocation(str(operator_idx) + '_retrieve:' + character, self.body_parts['ltm'], character)
				operator_idx += 1
				retrieve_target_location.execute()

				# We know the duration of LTM, but we do not add it to the schedule chart until it is shorter than visual search. 
				# Instead, start visual search. Any component of the visual search that is less than LTM retrieval will be included in the schedule chart.
				visual_search_duration = 0
				is_found = False

				while not(is_found) and (visual_search_duration < retrieve_target_location.duration):

					# Find which target we intersect with.
					intersecting_event = Event(self.body_parts['eyes'].fixation_x, self.body_parts['eyes'].fixation_y)
					intersecting_handler = handler.find_intersect(intersecting_event)

					if intersecting_handler is not None:
						# This should always be true; otherwise, we have gone out of the environment.
						encode_operator = Encode(str(operator_idx) + '_encode:' + intersecting_handler.name, self.body_parts['eyes'], intersecting_handler)
						schedule_chart.add_node(encode_operator)
						operator_idx += 1

						encode_operator.execute()
						visual_search_duration += encode_operator.duration

						schedule_chart.add_edge(previous_cognitive_operator, encode_operator)
						schedule_chart.add_edge(previous_visual_operator, encode_operator)

						previous_visual_operator = encode_operator

						if encode_operator.initiate_saccade:
							# We did not encode the handler under the fixation point in time and we need another saccade.
							move_eyes = Move(str(operator_idx) + '_motor_eyes:' + intersecting_handler.name, self.body_parts['eyes'], intersecting_handler)
							schedule_chart.add_node(move_eyes)
							operator_idx += 1

							move_eyes.execute()
							visual_search_duration += move_eyes.duration

							schedule_chart.add_edge(encode_operator, move_eyes)

							if previous_motor_eyes_operator is not None:
								schedule_chart.add_edge(previous_motor_eyes_operator, move_eyes)

							previous_motor_eyes_operator = move_eyes

						else:
							# We encoded the handler in time. Update LTM and VSTM.
							activate_target_location = ActivateTargetLocation(str(operator_idx) + '_activate:' + encode_operator.target.name, self.body_parts['ltm'], encode_operator.target.name, encode_operator.target)
							schedule_chart.add_node(activate_target_location)
							operator_idx += 1

							activate_target_location.execute()

							visual_search_duration += activate_target_location.duration

							schedule_chart.add_edge(previous_cognitive_operator, activate_target_location)
							schedule_chart.add_edge(encode_operator, activate_target_location)

							previous_cognitive_operator = activate_target_location

							# Now need to check if this is our target.
							if encode_operator.target.name == target.name:
								# We found the target and can move the finger to it.
								is_found = True
							else:
								# This was not what we were looking for. Continue visual search.

								# Keep picking a random point in the current handler around the current fixation point, until we find an handler area we have not visited. 
								current_fixation_x = self.body_parts['eyes'].fixation_x
								current_fixation_y = self.body_parts['eyes'].fixation_y

								is_found_unexplored = False
								while not is_found_unexplored:
									next_fixation_x = np.random.normal(current_fixation_x, self.visual_search_sigma)
									next_fixation_y = np.random.normal(current_fixation_y, self.visual_search_sigma)

									# Check if still within the boundaries of the handler.
									if self.handler.intersect(next_fixation_x, next_fixation_y):

										# Check if new search target already in visual memory, in which  case we should not jump there.
										if self.body_parts['vstm'].get

										is_found_unexplored = True

								move_eyes = Move(str(operator_idx) + '_motor_eyes:' + intersecting_handler.name, self.body_parts['eyes'], intersecting_handler)
								schedule_chart.add_node(move_eyes)
								operator_idx += 1

								move_eyes.execute()
								visual_search_duration += move_eyes.duration

								schedule_chart.add_edge(previous_cognitive_operator, move_eyes)

								if previous_motor_eyes_operator is not None:
									schedule_chart.add_edge(previous_motor_eyes_operator, move_eyes)

								previous_motor_eyes_operator = move_eyes

				move_finger = Move(str(operator_idx) + '_motor_finger:' + character, self.body_parts['thumb'], target)
				schedule_chart.add_node(move_finger)
				operator_idx += 1

				if not is_found:
					# Visual search could not find it before LTM. Add LTM-based congnitive operator to the schedule chart.
					schedule_chart.add_node(retrieve_target_location)

					# Move fixation to the target.
					move_eyes = Move(str(operator_idx) + '_motor_eyes:' + character, self.body_parts['eyes'], retrieve_target_location.symbol_location)
					schedule_chart.add_node(move_eyes)
					operator_idx += 1

					move_eyes.execute()

					if previous_cognitive_operator is not None:
						schedule_chart.add_edge(previous_cognitive_operator, retrieve_target_location)
					
					schedule_chart.add_edge(retrieve_target_location, move_eyes)
					schedule_chart.add_edge(move_eyes, move_finger)

					if previous_motor_eyes_operator is not None:
						schedule_chart.add_edge(previous_motor_eyes_operator, move_eyes)

					previous_cognitive_operator = retrieve_target_location

					previous_motor_eyes_operator = move_eyes

				if previous_cognitive_operator is not None:
						schedule_chart.add_edge(previous_cognitive_operator, move_finger)

				if previous_motor_finger_operator is not None:
					schedule_chart.add_edge(previous_motor_finger_operator, move_finger)

				previous_motor_finger_operator = move_finger

			previous_perceptual_operator = perceive_word

			word_count += 1

			# Reset every 3 words.
			if word_count > 2:
				word_count = 0

		return schedule_chart

	def draw(self,  ax):
		for body_part in self.body_parts.values():
			body_part.draw(ax)

class BodyPart(ABC):
	''' This is an abstract class represeting a body part (e.g., fingers, eyes). Body parts can have related body parts that they control (e.g., hand has fingers.)'''

	def __init__(self, name, location_x, location_y, handler=None):
		'''Initialize Body Part with a beginning location and a device that it is acting on (default None)'''
		self.name = name
		self.location_x = location_x
		self.location_y = location_y
		self.parent = None
		self.children = None
		self.handler = handler

	@abstractmethod
	def accept(self, operator):
		raise NotImplementedError("You should implement this!")

	def set_parent(self, parent):
		self.parent = parent
		if not self.parent.children.contains(self):
			self.parent.add_child(self)

	def add_child(self, child):
		if self.children is None:
			self.children = {}
		self.children[child.name] = child

		if not(child.parent == self):
			if child.parent:
				child.parent.remove_child(child)
			child.parent = self 

	def remove_child(self, child):
		if child.parent == self:
			if self.children:
				del self.children[child.name]
			child.parent = None

	def draw(self,  ax):
		pass

class LongTermMemory(BodyPart):
	def __init__(self, name):
		super(LongTermMemory, self).__init__(name, 0, 0)

		self.store = {}
		self.activations = {} # a dictonary of pairs containing last activation time and activation value keyed by symbols they represent.
		self.retrievel_noise = 0.60
		self.F = 1.06 #  a scaling factor for retrieval times.
		self.f = 1.53 # scaling of the effect of activation on retrieval time.
		self.d = 0.5  # decay (forgetting)

	def accept(self, cognitive_operator):
		''' LTM only accepts cognitive operators. '''

		if not isinstance(cognitive_operator, Cognitive):
			raise Exception('Operator is not a cognitive operator')  
		
		return cognitive_operator.visit_ltm(self)

	def put(self, symbol, value, timestamp):
		''' Simply updates the activation. This happens instantentiously. '''
		store[symbol] = value

		activation = None

		if symbol in self.activations.keys():
			activation = self.activations[symbol]
			t = timestamp - activation[0]
			activation = (timestamp, activation[1] + t**(-self.d))
		else:
			# This is the first time.
			activation = (timestamp, 0)

		self.activations[symbol] = activation

		return 0

	def get(self, symbol, timestamp):

		activation = None
		symbol_location = None

		if symbol in self.activations.keys():
			symbol_location = store[symbol]

			activation = self.activations[symbol]
			t = timestamp - activation[0]
			activation = (timestamp, activation[1] + t**(-self.d))

			B = math.log(activation[1])

			duration = self.F*math.exp(self.f*B)
		else:
			# This is the first time.
			activation = (timestamp, 0)

			# Cannot remember what you do not know.
			symbol_location = None
			duration = math.inf

		self.activations[symbol] = activation

		return (duration, symbol_location)

class ShortTermMemory(BodyPart):
	def __init__(self, name):
		super(ShortTermMemory, self).__init__(name, 0, 0)

		self.storage_capacity = 5
		self.decay_time = 4000
		self.store = {}
		self.store_timestamps = {}

	def accept(self, cognitive_operator):
		''' STM only accepts cognitive operators. '''

		if not isinstance(cognitive_operator, Cognitive):
			raise Exception('Operator is not a cognitive operator')  
		
		return cognitive_operator.visit_stm(self)

	def put(self, symbol, value, timestamp):
		pass

	def get(self, symbol, value, timestamp):
		pass

class Finger(BodyPart):
	''' Finger model. '''

	def __init__(self, name, location_x, location_y, handler=None):
		super(Finger, self).__init__(name, location_x, location_y, handler)
		self.a = 105.0 #TODO: set Fitts' Law parameter a
		self.b = 147.7 #TODO: set Fitts' Law parameter b
	
	def accept(self, motor_operator):
		'''Finger only accepts motor operators.'''
		if not isinstance(motor_operator, MotorOperator):
			raise Exception('Operator is not a motor operator')  
		
		return motor_operator.visit_finger(self)

	def move(self, target):
		''' Moves the  finger to the new location and returns the duration. '''

		target_x = target.top_left_x + target.width/2
		target_y = target.top_left_y + target.height/2

		A = math.sqrt( (self.location_x-target_x)**2 + (self.location_y-target_y)**2 )
		W = min([target.width, target.height])

		duration = self.a + self.b*math.log2(A/W+1)
		
		self.location_x = target_x
		self.location_y = target_y

		move_event = MoveBodyPartEvent(self, target_x, target_y)
		self.handler.handle(move_event)

		return duration
		
	def visit_button(self, button):
		return button.press()

	def draw(self,  ax):
		ax.add_patch(patches.Circle((self.location_x,self.location_y), 10, fill=True))

class Eyes(BodyPart):
	''' Eyes model. The location is the current fixation point. '''

	def __init__(self, name, location_x, location_y, handler_distance, handler=None):
		''' Initializes eyes, places them at a specific location at a specific distance from the handler, and sets the fixation point by projecting perpendicular to the handler plane. '''

		super(Eyes, self).__init__(name, location_x, location_y, handler)

		self.handler_distance = handler_distance

		self.t_prep = 200
		self.t_exec = 70
		self.t_sacc = 0.002

		self.fixation_x = location_x
		self.fixation_y = location_y
		
	
	def accept(self, motor_operator):
		'''Eyes only accepts motor operators.'''
		if not isinstance(motor_operator, MotorOperator):
			raise Exception('Operator is not a motor operator')  
		
		return motor_operator.visit_eyes(self)

	def move(self, target):
		''' Moves the fixartion point to the new location (performs a saccade) and returns the duration. '''

		target_x = target.top_left_x + target.width/2
		target_y = target.top_left_y + target.height/2

		duration = self.t_prep + self.t_exec + D*self.t_sacc
	
		self.fixation_x = target_x
		self.fixation_y = target_y

		move_event = MoveBodyPartEvent(self, target_x, target_y)
		self.handler.handle(move_event)

		return duration
		
	def visit_button(self, button):
		return button.see()

	def draw(self,  ax):
		ax.add_patch(patches.Circle((self.fixation_x,self.fixation_y), 100, fill=False))
