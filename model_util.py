#TODO Implement as a singleton
class EventHandler():
	def __init__(self, top_left_x, top_left_y, width, height):
		'''Top left (x,y) relative to parent'''
		self.children = []
		self.parent = None
		self.top_left_x = top_left_x
		self.top_left_y = top_left_y
		self.width = width
		self.height = height

	def handle(self, event):
		for child in self.children:
			if self.intersects(event.x, event.y, child):
				translated_event = self.translate(child, event)
				return child.handle(translated_event)
		return False
			
	def translate(self, child, event):
		translated_event = event.copy()
		translated_event.x = self.top_left_x - event.x 
		translated_event.y = self.top_left_y - event.y 

	def intersects(self, loc_x, loc_y, child):
		if (loc_x > child.top_left_x and loc_x < child.top_left_x + child.width) and (loc_y < child.top_left_y and loc_y > child.top_left_y - child.height):
			return True
		else:
			return False

	def add_child(self, child):
		if isinstance(child, EventHandler):
			if self.children is None:
				self.children = []
			self.children.append(child)

			if child.parent != self:
				if child.parent:
					child.parent.remove_child(child)
				child.parent = self 
		else:
			raise Exception('Trying to add incorrect type of child')

	def remove_child(self, child):
		if self.children:
			self.children.remove(child)
		child.parent = None

	def set_parent(self, parent):
		self.parent = parent
		if not self.parent.children.contains(self):
			self.parent.add_child(self)

class BodyPartEvent():
	def __init__(self):
		pass

# class MiniMap():
	
# 	def __init__(self):
# 		self.uiLayerMap = []
		
# 	def initDefaultMap(self):
# 		#TODO init any default layout to map[]
# 		#? how to represent the map
# 		pass
	
# 	# getter for component on locationX/Y location
# 	def getComponent(self, locationX, locationY):
# 		return self.uiLayerMap[locationX][locationY]

# 	def deviceAccept(self, locationX, locationY):
# 		self.uiLayerMap[locationX][locationY].accept()




class MoveBodyPartEvent():
	def __init__(self, body_part, x, y):
		self.body_part = body_part
		self.x = x
		self.y = y
	
	def move(self):
		pass
		# if finger overlap with the correct location 
		# miniMap = MiniMap()
		# if miniMap.getComponent(self.body_part.locationX, self.body_part.locationY):
		# 	miniMap.deviceAccept(self.body_part.locationX, self.body_part.locationY)
	
	def copy(self):
		return MoveBodyPartEvent(self.body_part, self.x, self.y)