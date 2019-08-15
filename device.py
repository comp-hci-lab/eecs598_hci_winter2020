from model_util import EventHandler
from abc import ABCMeta, abstractmethod
from interface import Button

class Device(EventHandler):

    def __init__(self, top_left_x, top_left_y, width, height):
        super().__init__(top_left_x, top_left_y, width, height)

	
    def create_touchScreen(self, top_left_x, top_left_y, width, height):
        return TouchScreen(top_left_x, top_left_y, width, height)


class Screen(Device):

	def __init__(self):
		pass

class TouchScreen(Screen):
	
	def __init__(self, top_left_x, top_left_y, width, height):
		self.top_left_x = top_left_x
		self.top_left_y = top_left_y
		self.width = width
		self.height = height
	
	def create_Button(self, top_left_x, top_left_y, width, height):
		return Button(top_left_x, top_left_y, width, height)



	def handle(self, event):
		pass
		# if isinstance(event, InputEvent):
		# 	return self.input_widget.handle(event)
 


# class Mouse(Device):

# 	def __init__(self):
		# self._left_button = Button()
		# self._right_button = Button()
		# self._scroll = Scroll()


# class Keyboard(Device):

# 	def __init__(self, location_x, location_y, keyboard_file):
# 		self.keyboard_file = keyboard_file
# 		self.type = "keyboard"
		
# 		#Set keyboard location, should be static
# 		self.location_x = location_x
# 		self.location_y = location_y

# 		#Change to multiple buttons array
# 		# self._keys = Button()
# 		# self.set_keys()


# 	def set_keys(self):
# 		pass


# 	#change keys to given key location file
# 	def change_keys(self, new_keyboard_file):
# 		pass




