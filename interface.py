class Interface():

	def __init__(self):
		pass


class Input_Widget(Interface):

	def __init__(self):
		pass

class Output_Widget(Interface):

	def  __init__(self):
		pass

class Button(Input_Widget):

	def __init__(self, location_x, location_y, type="button"):
		self.location_x = location_x
		self.location_y = location_y
		self.type = type
		self.state = False

	'''Change state of device to pressed, if successful'''
	def press(self, curr_x, curr_y):
		if curr_x == location_x && curr_y == location_y:
			self.state = True
			'''Add pressing action to critical path/schedule chart'''