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


class Haptic(Perceptual):


class Cognitive(Operator):

	def __init__(self):
		#Have access to LTM/STM
		self.long_term_memory = LongTermMemory()



class Motor(Operator):

	def __init__(self):



class Memory():

	def __init__(self, newPiece):
		self.newPiece = newPiece

class LongTermMemory(Memory):

	def __init__(self, newPiece):
		super().__init__(newPiece)


class ShortTermMemory(Memory):

	def __init__(self, newPiece):
		super().__init__(newPiece)
		self.STM = []
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
	#Implement Fitts Law in this class
	def __init__(self):

	def fittsLaw(self):

class Eyes():
	#Implement Visual Search in this class
	def __init__(self):

	def visualSearch(self):