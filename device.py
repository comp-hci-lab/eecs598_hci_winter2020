from model_util import EventHandler
from interface import Interface, Button

class Device(EventHandler):
	def __init__(self, name, label, top_left_x, top_left_y, width, height):
		super(Device, self).__init__(name, label, top_left_x, top_left_y, width, height)
		
class TouchScreenDevice(Device):
	def __init__(self, name, label, top_left_x, top_left_y, width, height):
		super(TouchScreenDevice, self).__init__(name, label, top_left_x, top_left_y, width, height)
		
	def create_screen(self, name, label, top_left_x, top_left_y, width, height):
		return TouchScreen(name, label, top_left_x, top_left_y, width, height)

class Screen(EventHandler):

	def __init__(self, name, label, top_left_x, top_left_y, width, height):
		super(Screen, self).__init__(name, label, top_left_x, top_left_y, width, height)

class TouchScreen(Screen):
	
	def __init__(self, name, label, top_left_x, top_left_y, width, height):
		super(TouchScreen, self).__init__(name, label, top_left_x, top_left_y, width, height)

class DeviceBuilder:

	def __init__(self):
		self.device = None

	def set_screen(self, screen, top_left_x, top_left_y):
		'''Setting to default locations'''
		self.device.add_child(screen, top_left_x, top_left_y)
		return self

	def get_result(self):
		return self.device

class TouchScreenDeviceBuilder(DeviceBuilder):
	
	def __init__(self, name, label, top_left_x, top_left_y, width, height):
		self.device = TouchScreenDevice(name, label, top_left_x, top_left_y, width, height)

class TouchScreenKeyboardDeviceDirector:
	@staticmethod
	def construct(name, label, top_left_x, top_left_y, width, height, h_bezel, v_bezel):
		touch_screen_device_builder = TouchScreenDeviceBuilder(name, label, top_left_x, top_left_y, width, height)
		
		# Place a screen on the device.
		screen = touch_screen_device_builder.device.create_screen('touchscreen', 'touchscreen', top_left_x + h_bezel, top_left_y + v_bezel, width - 2*h_bezel, height - 2*v_bezel)

		# Place a keyboard at the bottom third of the device.
		keyboard = Interface('keyboard', 'keyboard', 0, 2*screen.height/3, screen.width, screen.height/3)

		screen.add_child(keyboard, 0, 2*screen.height/3)

		# Add keys.
		default_key_width = keyboard.width/10
		default_key_height = keyboard.height/4
		space_key_width = default_key_width*3
		del_key_width = (keyboard.width - (default_key_width*7))/2

		key_rows = [['q','w','e','r','t','y','u','i','o','p'],['a','s','d','f','g','h','j','k','l'],['z','x','c','v','b','n','m'],[' ']]

		# Starting key positions.
		key_top_left_x = 0
		key_top_left_y = 0

		for key_row in key_rows:
			key_width = default_key_width
			key_height = default_key_height

			if len(key_row) == 1:
				# This is a space.
				key_width = space_key_width

			key_top_left_x = (keyboard.width - len(key_row)*key_width)/2

			for key in key_row:
				key_button = Button(key, key, key_top_left_x, key_top_left_y, key_width, key_height)

				keyboard.add_child(key_button, key_top_left_x, key_top_left_y)

				key_top_left_x += key_width

			# If this is the  bottom row, add del key at the end.
			if len(key_row) == 7:
				del_button = Button('del', 'del', key_top_left_x, key_top_left_y, del_key_width, key_height)
				keyboard.add_child(del_button, key_top_left_x, key_top_left_y)				

			key_top_left_y += default_key_height

		return touch_screen_device_builder.set_screen(screen, screen.top_left_x, screen.top_left_y).get_result()

