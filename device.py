from model_util import EventHandler
from abc import ABCMeta, abstractmethod
from interface import Button

class Device(EventHandler):
	def __init__(self, name, top_left_x, top_left_y, width, height):
		super().__init__(name, top_left_x, top_left_y, width, height)
		
	def create_screen(self, top_left_x, top_left_y, width, height):
		pass

class Screen(EventHandler):

	def __init__(self):
		pass
	
	def create_button(self, top_left_x, top_left_y, width, height):
		return Button(top_left_x, top_left_y, width, height)

class TouchScreen(Screen):
	
	def __init__(self, top_left_x, top_left_y, width, height):
		self.top_left_x = top_left_x
		self.top_left_y = top_left_y
		self.width = width
		self.height = height
	




	def handle(self, event):
		pass
		# if isinstance(event, InputEvent):
		# 	return self.input_widget.handle(event)
 

# class AbstractDeviceFactory:
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


class DeviceBuilder:
	__metaclass__ = ABCMeta

	@abstractmethod
	def __init__(self):
		self.device = None

	@abstractmethod
	def set_screen(self, value):
		pass

class TouchScreenDevice(Device):
	def __init__(self, top_left_x, top_left_y, width, height):
		super().__init__(top_left_x, top_left_y, width, height)
		
	def create_screen(self, top_left_x, top_left_y, width, height):
		return TouchScreen(top_left_x, top_left_y, width, height)

class TouchScreenDeviceBuilder(DeviceBuilder):
	
	def __init__(self, top_left_x, top_left_y, width, height):
		self.device = TouchScreenDevice(top_left_x, top_left_y, width, height)

	def set_screen(self, value):
		'''Setting to default locations'''
		self.device.add_child(value, 0, 0)
		return self
	
	def get_result(self):
		return self.device

class TouchScreenDeviceDirector:
	@staticmethod
	def construct(top_left_x, top_left_y, width, height):
		touch_screen_device_builder = TouchScreenDeviceBuilder(top_left_x, top_left_y, width, height)
		return touch_screen_device_builder.set_screen(touch_screen_device_builder.device.create_screen()).get_result()