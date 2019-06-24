class Operator():
	#All operators use this as base
	def __init__(self):

	def execute():
		#Return a set of properties for what happens when you execute it (Time, cycle, etc)
		#should return a snapshot of what is going on at that time along with how long it took


class Perceptual(Operator):

	def __init__(self, storage):
		#Initialize Perceptual values
		#Need access to some sort of some storage
		self.storage = storage
		
class Visual(Perceptual):

	def __init__(self):

	def execute():


class Auditory(Perceptual):

	def __init__(self):

	def execute():


class Haptic(Perceptual):

	def __init__(self):

	def execute():


class Cognitive(Operator):

	def __init__(self):
		#Have access to LTM/STM
		self.long_term_memory = LongTermMemory()
		self.short_term_memory = ShortTermMemory()

	def execute():



class Motor(Operator):

	def __init__(self):


	def execute():



class Memory():

	def __init__(self, newPiece=None):
		if newPiece:
			self.newPiece = newPiece

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

	def addToMemory(self, newPiece):
		if self.newPiece in self.STM:
				self.STM.remove(self.newPiece)
				self.STM.insert(self.newPiece)
		elif len(self.STM) > 3:
			self.STM.append(self.newPiece)
		else:
			self.STM.pop()
			self.STM.append(self.newPiece)

class Fingers():
	
	def __init__(self):


class Eyes():
	#Implement Visual Search in this class
	def __init__(self):

	def visualSearch(self):