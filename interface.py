class Interface():

	def __init__(self):


class Input_Widget(Interface):

	def __init__(self):


class Output_Widget(Interface):

	def  __init__(self):


class Mouse(Input_Widget):

	def __init__(self):


class Keyboard(Input_Widget):

	def __init__(self, keyboard_file):
		self.keyboard_file = keyboard_file
		set_keys()


	def set_keys(self):


	#change keys to given key location file
	def change_keys(self, new_keyboard_file):


class Screen(Input_Widget):

	def __init__(self):