from abc import ABC, ABCMeta, abstractmethod

class Human(): 

	def __init__(self):
		pass

	@abstractmethod
	def add_hands(self):
		raise NotImplementedError("You should implement this!")

	@abstractmethod
	def add_eyes(self):
		raise NotImplementedError("You should implement this!")

	@abstractmethod
	def add_ears(self):
		raise NotImplementedError("You should implement this!")

	@abstractmethod
	def add_memory(self):
		raise NotImplementedError("You should implement this!")

class BodyPart(ABC):

	def __init__(self, location_x, location_y, device=None, handler):
		'''Initialize Body Part with a beginning location and a device that it is acting on (default None)'''
		self.location_x = location_x
		self.location_y = location_y
		self.device = device
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
			self.children = []
		self.children.append(child)

		if child.parent != self:
			if child.parent:
				child.parent.remove_child(child)
			child.parent = self 

	def remove_child(self, child):
		if self.children:
			self.children.remove(child)
		child.parent = None


class Arm(BodyPart):

	def __init__(self, location_x, location_y, is_dominant, device=None, handler):
		super().__init__(location_x, location_y, handler)
		self.location_x = location_x
		self.location_y = location_y
		self.device = device
		self.parent = None
		self.children = None

	'''Move arm and its children'''
	def accept(self, new_location_x, new_location_y):
		if motor_operator not isinstance(motor_operator, MotorOperator):
			#TODO Throw an exception
			pass

		if motor_operator.type == 'move':
			change_x = new_location_x - self.location_x
			change_y = new_location_y - self.location_y
			self.location_x = self.location_x + change_x
			self.location_y = self.location_y + change_y
			if self.children:
				for child in self.children:
					child.accept(child.location_x + change_x, child.location_y + change_y)

class Hand(BodyPart):

	def __init__(self, location_x, location_y, is_dominant, device=None, handler):
		super().__init__(location_x, location_y, device, handler)
		self.location_x = location_x
		self.location_y = location_y
		self.is_dominant = is_dominant
		self.device = device
		self.parent = None
		self.children = None

	'''Move hand and its children'''
	def accept(self, motor_operator):
		if motor_operator not isinstance(motor_operator, MotorOperator):
			#TODO Throw an exception
			pass
		if motor_operator.type == 'move':
			change_x = new_location_x - self.location_x
			change_y = new_location_y - self.location_y
			self.location_x = self.location_x + change_x
			self.location_y = self.location_y + change_y
			if self.children:
				for child in self.children:
					child.accept(child.location_x + change_x, child.location_y + change_y)

class Builder():
	__metaclass__ = ABCMeta

	@abstractmethod
	def set_location_x(self, value):
		pass

	@abstractmethod
	def set_location_y(self, value):
		pass

	@abstractmethod
	def set_device(self, value):
		pass

	@abstractmethod
	def set_is_dominant(self, value):
		pass


class HandBuilder(Builder):

	def __init__(self):
		self.hand = Hand()

	def set_location_x(self, value):
		self.hand.location_x = value
		return self

	def set_location_y(self, value):
		self.hand.location_y = value
		return self

	def set_device(self, value):
		self.hand.device = value
		return self

	def set_is_dominant(self, value):
		self.hand.is_dominant = value
		return self


class HandBuilderDirector(BodyPart):
	@staticmethod
	def construct(location_x, location_y, device, is_dominant):
		return HandBuilder().set_location_x(location_x).set_location_y(location_y).set_device(device).set_is_dominant(is_dominant)

class Finger(BodyPart):

	def __init__(self, location_x, location_y, device=None, handler):
		super().__init__(location_x, location_y, device, handler)
		self.location_x = location_x
		self.location_y = location_y
		self.held_device = device
		self.parent = None
		self.children = None
	
	def accept(self, motor_operator):
		if not isinstance(motor_operator, MotorOperator):
			#TODO Throw an exception
			pass
		motor_operator.visitFinger()

	def move(self, new_location_x, new_location_y):
		self.location_x = new_location_x
		self.location_y = new_location_y

		move_event = MoveBodyPartEvent(self)
		self.handler.handle(move_event)

		# if motor_operator.type == 'press':
		# 	'''Check to see if button is at location, if present press'''
		# 	if self.location_x != motor_operator.new_location_x or self.location_y != motor_operator.new_location_y:
		# 		'''Perform a move operator if locations aren't same'''
		# 		self.location_x = motor_operator.new_location_x
		# 		self.location_y = motor_operator.new_location_y
		# 	if self.held_device == None:
		# 		device = check_for_device(motor_operator.new_location_x, motor_operator.new_location_y)
		# 	if device == None or device.type != 'button':
		# 		'''If no device or non button device found at location'''
		# 		pass
		# 	device.press()
		# else if self.held_device == None and type == 'grasp':
		# 	if self.location_x != new_location_x and self.location_y != new_location_y:
		# 		'''Perform a move operator if locations aren't same'''
		# 		self.location_x = motor_operator.new_location_x
		# 		self.location_y = motor_operator.new_location_y
		# 	grasp()
		# else if type == 'move':
		# 	self.location_x = motor_operator.new_location_x
		# 	self.location_y = motor_operator.new_location_y
		# 	if self.held_device != None:
		# 		self.held_device.move(self.location_x, self.location_y, new_location_x, new_location_y)

	# def grasp(self):
	# 	self.device = check_for_device(location_x, location_y)

class Eyes(BodyPart):

	def __init__(self, location_x, location_y, device=None, handler):
		super().__init__(location_x, location_y, device, handler)
		self.location_x = location_x
		self.location_y = location_y
		self.device = device

	'''Change what is in the sight line of the user'''
	def accept(self, motor_operator):
		if motor_operator not isinstance(motor_operator, MotorOperator):
			#TODO Throw an exception
			pass
		if motor_operator.type == 'move':
			self.location_x = new_location_x
			self.location_y = new_location_y
			send()

	'''Send information of what's in sight line as a visual operator'''
	def send(self):
		cogn_operator.execute(devices[location_x][location_y])

class Ears(BodyPart):

	def __init__(self, location_x, location_y, device=None, handler):
		super().__init__(location_x, location_y, device, handler)
		self.location_x = location_x
		self.location_y = location_y
		self.device = device

	'''Send information of what's heard as an auditory operator'''
	def send(self):
		cogn_operator.execute(devices[location_x][location_y])

class Memory(Human):

	def __init__(self, newPiece=None):
		if newPiece:
			self.newPiece = newPiece

	'''Operator is a visitor that is allowed or not to operate on the memory, acceptable types are perceptual or cognitive'''
	def accept(self, operator):
		pass

	'''Send out operator from memory, acceptable types are cognitive or motor'''
	def send(self, operator):
		pass

class LongTermMemory(Memory):

	def __init__(self, newPiece=None):
		super().__init__(newPiece)
		self.LTM = []
		if newPiece:
			addToMemory(newPiece)

	def addToMemory(self, newPiece):
		self.LTM.append(newPiece)


class ShortTermMemory(Memory):

	def __init__(self, newPiece=None):
		super().__init__(newPiece)
		self.STM = []
		if newPiece:
			addToMemory(newPiece)

	'''Operator is a visitor that is allowed or not to operate on the memory, acceptable types are perceptual or cognitive'''
	def accept(self, operator):
		if operator not isinstance(operator, CognitiveOperator) and operator not isinstance(operator, PerceptualOperator):
			#TODO Throw an exception
			pass

	'''Send out operator from memory, acceptable types are cognitive or motor'''
	def send(self, operator):
		pass

	def addToMemory(self, newPiece):
		pass

class VisualShortTermMemory(ShortTermMemory):

	def __init__(self):
		super().__init__()
		self.vSTM = []

	'''Modify accept to only take in visual operators'''
	def accept(self, item):
		self.addToMemory(item)

	def addToMemory(self, newPiece):
		if newPiece in self.vSTM:
				self.vSTM.remove(newPiece)
				self.vSTM.insert(newPiece)
		elif len(self.vSTM) > 3:
			self.vSTM.append(newPiece)
		else:
			self.vSTM.pop()
			self.vSTM.append(newPiece)
		

class AuditoryShortTermMemory(ShortTermMemory):

	def __init__(self):
		super().__init__()
		self.aSTM = []


	'''Modify accept to only take in auditory operators'''
	def accept(self, item):
		self.addToMemory(item)

	def addToMemory(self, newPiece):
		if newPiece in self.aSTM:
				self.aSTM.remove(newPiece)
				self.aSTM.insert(newPiece)
		elif len(self.aSTM) > 3:
			self.aSTM.append(newPiece)
		else:
			self.aSTM.pop()
			self.aSTM.append(newPiece)
		

class HapticShortTermMemory(ShortTermMemory):

	def __init__(self):
		super().__init__()
		self.hSTM = []

	'''Modify accept to only take in haptic operators'''
	def accept(self, item):
		self.addToMemory(item)

	def addToMemory(self, newPiece):
		if newPiece in self.hSTM:
				self.hSTM.remove(newPiece)
				self.hSTM.insert(newPiece)
		elif len(self.hSTM) > 3:
			self.hSTM.append(newPiece)
		else:
			self.hSTM.pop()
			self.hSTM.append(newPiece)
		
