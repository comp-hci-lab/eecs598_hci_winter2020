#TODO Implement as a singleton
class BodyPartHandler():
	def __init__(self):
		self.devices = []

	def register_device(self, device):
		#TODO This function
		self.devices.append(device)


	def handle(self, event):
		if isinstance(event, MoveBodyPartEvent):
			#TODO Check for all of the available devices and see if the new location of the move body part event body part is intersecting with that device and then let the device handle that event


class BodyPartEvent():
	def __init__(self):
		pass