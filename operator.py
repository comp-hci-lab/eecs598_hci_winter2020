class Operator():
	#All operators use this as base
	def __init__(self):

	def execute():
		#Return a set of properties for what happens when you execute it (Time, cycle, etc)


class Perceptual(Operator):

	def __init__(self):
		#Initialize Perceptual values
		


	def inputIsWord(self):
		#Given input is word
		self.isWord = True


class Visual(Perceptual):


class Auditory(Perceptual):


class Haptic(Perceptual):


class Cognitive(Operator):

	def __init__(self, item, uniq_id, dependent, start_time, end_time):
		#Initialize Perceptual values
		super().__init__(item, uniq_id, dependent, start_time, end_time)


class Motor(Operator):

	def __init__(self, item, uniq_id, dependent, start_time, end_time):
		#Initialize Perceptual values
		super().__init__(item, uniq_id, dependent, start_time, end_time)


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