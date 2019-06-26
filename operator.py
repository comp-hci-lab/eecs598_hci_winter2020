class Operator():
	#All operators use this as base
	def __init__(self):

	def execute(self):
		#Return a set of properties for what happens when you execute it (Time, cycle, etc)
		#should return a snapshot of what is going on at that time along with how long it took


class Perceptual(Operator):

	def __init__(self, storage):
		#Initialize Perceptual values
		#Need access to some sort of some storage
		self.storage = storage
		
class Visual(Perceptual):

	def __init__(self):

	def execute(self):


class Auditory(Perceptual):

	def __init__(self):

	def execute(self):


class Haptic(Perceptual):

	def __init__(self):

	def execute(self):


class Cognitive(Operator):

	def __init__(self):
		#Have access to LTM/STM
		self.long_term_memory = LongTermMemory()
		self.short_term_memory = ShortTermMemory()

	def execute(self):



class Motor(Operator):

	def __init__(self):


	def execute(self):



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

class Hand():

	def __init__(self):


	def move_mouse():


class Right_Hand(Hand):
	
	def __init__(self):

	#Change what is within reach of user's fingers
	def move_fingers(self):


class Left_Hand(Hand):

	def __init__(self):

	#Change what is within reach of user's fingers
	def move_fingers(self):


class Eyes():

	def __init__(self):

	#Change what is in the sight line
	def move_eyes(self):

class Visual_Search():

	def __init__(self):
		self.letter_freq = []
		set_frequency()

	def set_frequency(self):
		letter_freq["e"] = 11.1607/100
        letter_freq["a"] = 8.4966/100
        letter_freq["r"] = 7.5809/100
        letter_freq["i"] = 7.5448/100
        letter_freq["o"] = 7.1635/100
        letter_freq["t"] = 6.9509/100
        letter_freq["n"] = 6.6544/100
        letter_freq["s"] = 5.7351/100
        letter_freq["l"] = 5.4893/100
        letter_freq["c"] = 4.5388/100
        letter_freq["u"] = 3.6308/100
        letter_freq["d"] = 3.3844/100
        letter_freq["p"] = 3.1671/100
        letter_freq["m"] = 3.0129/100
        letter_freq["h"] = 3.0034/100
        letter_freq["g"] = 2.4705/100
        letter_freq["b"] = 2.0720/100
        letter_freq["f"] = 1.8121/100
        letter_freq["y"] = 1.7779/100
        letter_freq["w"] = 1.2899/100
        letter_freq["k"] = 1.1016/100
        letter_freq["v"] = 1.0074/100
        letter_freq["x"] = .2902/100
        letter_freq["z"] = .2722/100
        letter_freq["j"] = .1965/100
        letter_freq["q"] = .1962/100

class Fitts_Law():

	def __init__(self):
		initialize_keys()

	def initialize_keys(self):

