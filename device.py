from model_util import EventHandler
from interface import Interface, Button, KeyboardKey, KeyboardDeleteKey, TextBox

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

		default_textbox_margin = 10
		default_textbox_width = screen.width - 2*default_textbox_margin
		default_textbox_height = ((screen.width - 10) / 30) + 20
		default_textbox_character_width = (screen.width - 10) / 30
		default_textbox_character_height = (screen.width - 10) / 30

		# Place a textbox with transciprion phrase at the top of the screen.
		phrase_textbox = TextBox('phrase_textbox', '', default_textbox_margin, default_textbox_margin, default_textbox_width, default_textbox_height, default_textbox_character_width, default_textbox_character_height)
		screen.add_child(phrase_textbox, default_textbox_margin, default_textbox_margin)

		# Place a textbox with transciprion phrase at the top of the screen.
		transcript_textbox = TextBox('transcription_textbox', '', default_textbox_margin, default_textbox_margin + phrase_textbox.top_left_y + phrase_textbox.height, default_textbox_width, default_textbox_height, default_textbox_character_width, default_textbox_character_height)
		screen.add_child(transcript_textbox, default_textbox_margin, default_textbox_margin + phrase_textbox.top_left_y + phrase_textbox.height)

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
				key_button = KeyboardKey(key, key, key_top_left_x, key_top_left_y, key_width, key_height, transcript_textbox)

				keyboard.add_child(key_button, key_top_left_x, key_top_left_y)

				key_top_left_x += key_width

			# If this is the  bottom row, add del key at the end.
			if len(key_row) == 7:
				del_button = KeyboardDeleteKey('del', 'del', key_top_left_x, key_top_left_y, del_key_width, key_height, transcript_textbox)
				keyboard.add_child(del_button, key_top_left_x, key_top_left_y)				

			key_top_left_y += default_key_height

		return touch_screen_device_builder.set_screen(screen, screen.top_left_x, screen.top_left_y).get_result()

