class Interface():

	def __init__(self, devices):
		self.devices = {}

	def add_device(self, location_x, location_y, device_type):
		self.devices[location_x] = {location_y: device_type} 

	def check_for_device(self, location_x, location_y):
		if location_x in self.devices:
			if location_y in self.devices[location_x]:
				return self.devices[location_x][location_y]
		return None


	def move(self, original_x, original_y, new_location_x, new_location_y):
		device_type = self.devices[original_x][original_y]
		del self.devices[original_x][original_y]
		self.add_device(new_location_x, new_location_y, device_type)


class Input_Widget(Interface):

	def __init__(self, location_x, location_y):
		self.location_x = location_x
		self.location_y = location_y

class Output_Widget(Interface):

	def  __init__(self):
		pass
