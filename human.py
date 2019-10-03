from abc import ABC, ABCMeta, abstractmethod
from model_util	import MoveBodyPartEvent
from operators import MotorOperator, Move
import networkx as nx
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Human(): 
	''' This class represents a human with both cognition and body. In Assignment 2, this will be an abstraction where most complex aspects of the human will be removed, except body parts. '''
	def __init__(self, handler = None):
		self.body_parts = {}
		self.handler = handler

	def add_body_part(self, body_part):
		self.body_parts[body_part.name] = body_part

	def create_finger(self, name, location_x, location_y):
		'''  Creates and adds a new figure to  the human. '''
		finger = Finger(name, location_x, location_y, self.handler)
		self.add_body_part(finger)
		return finger

	def press(self, input):
		''' Instructs the human to press on a series of targets. The human implementation simulates and predict behavior and returns a resulting schedule chart. Clients can then evaluate the schedule chart for duration of operations.'''
		schedule_chart = nx.DiGraph()

		# TODO: Add operators to the graph. For each motor operator, find the key by using handler.find_descendant(), then move thumb to the position of the key in the  handler.

		operator_idx = 0
		previous_operator = None

		for character in input:
			target = self.handler.find_descendant(character)

			move_finger = Move(str(operator_idx) + '_move:' + character, self.body_parts['thumb'], target)

			schedule_chart.add_node(move_finger)

			if previous_operator is not None:
				schedule_chart.add_edge(previous_operator, move_finger)

			operator_idx += 1
			previous_operator = move_finger

		return schedule_chart

	def draw(self,  ax):
		for body_part in self.body_parts.values():
			body_part.draw(ax)

class BodyPart(ABC):

	def __init__(self, name, location_x, location_y, handler=None):
		'''Initialize Body Part with a beginning location and a device that it is acting on (default None)'''
		self.name = name
		self.location_x = location_x
		self.location_y = location_y
		self.parent = None
		self.children = None
		self.handler = handler

	@abstractmethod
	def accept(self, motor_operator):
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
		''' Moves the  finger to the new location and returns the duration. Note that the move is perfectly executed without any noise.'''

		target_x = target.top_left_x + target.width/2
		target_y = target.top_left_y + target.height/2

		A = math.sqrt( (self.location_x-target_x)**2 + (self.location_y-target_y)**2 )
		W = min([target.width, target.height])

		duration = self.a + self.b*math.log2(A/W+1) #TODO: calculate duration using Fitts' Law.
	
		
		self.location_x = target_x
		self.location_y = target_y

		move_event = MoveBodyPartEvent(self, target_x, target_y)
		self.handler.handle(move_event)

		return duration
		
	def visit_button(self, button):
		return button.press()

	def draw(self,  ax):
		ax.add_patch(patches.Circle((self.location_x,self.location_y), 10, fill=True))
