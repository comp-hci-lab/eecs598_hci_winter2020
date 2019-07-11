class Device():

	def __init__(self): 
		pass


class Mouse(Device):

	def __init__(self):
		self._left_button = Button()
		self._right_button = Button()
		self._scroll = Scroll()


class Keyboard(Device):

	def __init__(self, location_x, location_y, keyboard_file):
		self.keyboard_file = keyboard_file
		self.type = "keyboard"
		
		#Set keyboard location, should be static
		self.location_x = location_x
		self.location_y = location_y

		#Change to multiple buttons array
		self._keys = Button()
		set_keys()


	def set_keys(self):
		pass


	#change keys to given key location file
	def change_keys(self, new_keyboard_file):
		pass


class Screen(Device):

	def __init__(self):
		pass