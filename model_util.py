#TODO Implement as a singleton
class BodyPartHandler():
	def __init__(self):
		self.devices = []

	def register_device(self, device):
		#TODO This function
		self.devices.append(device)


	def handle(self, event):
		if isinstance(event, MoveBodyPartEvent):
			#TODO Check for all of the available devices and see if the new location 
			#of the move body part event body part is intersecting with that device 
			#and then let the device handle that event
			pass

class BodyPartEvent():
	def __init__(self):
		pass

class MiniMap():
	
	def __init__(self):
		self.uiLayerMap = []
		
	def initDefaultMap(self):
		#TODO init any default layout to map[]
		#? how to represent the map
		pass
	
	# getter for component on locationX/Y location
	def getComponent(self, locationX, locationY):
		return self.uiLayerMap[locationX][locationY]

	def deviceAccept(self, locationX, locationY):
		self.uiLayerMap[locationX][locationY].accept()




class MoveBodyPartEvent():
	def __init__(self, body_part):
		self.body_part = body_part
	
	def move(self):
		# if finger overlap with the correct location 
		miniMap = MiniMap()
		if miniMap.getComponent(self.body_part.locationX, self.body_part.locationY):
			miniMap.deviceAccept(self.body_part.locationX, self.body_part.locationY)
	


	 