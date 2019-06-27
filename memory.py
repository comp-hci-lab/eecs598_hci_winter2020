class Memory():

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
		