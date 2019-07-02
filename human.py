class Human():

	def __init__(self):
		pass


class BodyPart(Human):

	def __init__(self, location_x, location_y, device=None):
		'''Initialize Body Part with a beginning location and a device that it is acting on (default None)'''
		self.location_x = location_x
		self.location_y = location_y
		self.device = device

	def accept(self, motor_operator):
		pass


class Hand(BodyPart):

	def __init__(self, location_x, location_y, device=None):
		super().__init__(location_x, location_y, device)
		self.location_x = location_x
		self.location_y = location_y
		self.device = device

	'''Move interface with it, if it has one with it'''
	def accept(self, motor_operator):
		pass

class Finger(Hand):

	def __init__(self, location_x, location_y, device=None):
		super().__init__(location_x, location_y, device)
		self.location_x = location_x
		self.location_y = location_y
		self.device = device

	'''Move interface with it, if it has one with it'''
	def accept(self, motor_operator):
		pass


class Right_Hand(Hand):
	
	def __init__(self, location_x, location_y, device=None):
		super().__init__(location_x, location_y, device)
		self.location_x = location_x
		self.location_y = location_y
		self.device = device

	#Change what is within reach of user's hand
	def accept(self, motor_operator):
		pass


class Left_Hand(Hand):

	def __init__(self, location_x, location_y, device=None):
		super().__init__(location_x, location_y, device)
		self.location_x = location_x
		self.location_y = location_y
		self.device = device

	#Change what is within reach of user's hand
	def accept(self, motor_operator):
		pass


class Eyes(BodyPart):

	def __init__(self, location_x, location_y, device=None):
		super().__init__(location_x, location_y, device)
		self.location_x = location_x
		self.location_y = location_y
		self.device = device

	'''Change what is in the sight line of the user'''
	def accept(self, motor_operator):
		pass

	'''Send information of what's in sight line as a visual operator'''
	def send(self, visual_operator):
		pass

class Ears(BodyPart):

	def __init__(self, location_x, location_y, device=None):
		super().__init__(location_x, location_y, device)
		self.location_x = location_x
		self.location_y = location_y
		self.device = device

	'''Send information of what's heard as an auditory operator'''
	def send(send, auditory_operator):
		pass

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
		pass

	'''Send out operator from memory, acceptable types are cognitive or motor'''
	def send(self, operator):
		pass

	def addToMemory(self, newPiece):
		if self.newPiece in self.STM:
				self.STM.remove(self.newPiece)
				self.STM.insert(self.newPiece)
		elif len(self.STM) > 3:
			self.STM.append(self.newPiece)
		else:
			self.STM.pop()
			self.STM.append(self.newPiece)

class VisualShortTermMemory(ShortTermMemory):

	def __init__(self):
		super().__init__()

	'''Modify accept to only take in visual operators'''
	def accept(self, operator):
		pass
		

class AuditoryShortTermMemory(ShortTermMemory):

	def __init__(self):
		super().__init__()

	'''Modify accept to only take in auditory operators'''
	def accept(self, operator):
		pass


class HapticShortTermMemory(ShortTermMemory):

	def __init__(self):
		super().__init__()

	'''Modify accept to only take in haptic operators'''
	def accept(self, operator):
		pass
		
