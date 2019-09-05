from model_util import EventHandler
from abc import ABCMeta, abstractmethod

class Interface(EventHandler):

    def __init__(self, name, top_left_x, top_left_y, width, height):
        super().__init__(name,top_left_x, top_left_y, width, height)

class Input_Widget(Interface):

    def __init__(self, name,top_left_x, top_left_y, width, height):
        super().__init__(name,top_left_x, top_left_y, width, height)


class Output_Widget(Interface):

    def __init__(self, name, top_left_x, top_left_y, width, height):
        super().__init__(name,top_left_x, top_left_y, width, height)


class Button(Input_Widget):
	def __init__(self, top_left_x, top_left_y, width, height):
		super(Button, self).__init__(top_left_x, top_left_y, width, height)
		self.state = False
	
	def handle(self, event):
		return self.accept(event.body_part)

	def accept(self, body_part):
		return body_part.visitButton(self)

	'''Change state of device to pressed, if successful'''
	def press(self):
		self.state = True
		'''Add pressing action to critical path/schedule chart'''
		'''Send output'''

	
class InterfaceBuilder:
	__metaclass__ = ABCMeta

	@abstractmethod
	def __init__(self):
		self.interface = None

	@abstractmethod
	def add_button(self, value):
		pass


class GUIBuilder(InterfaceBuilder):

	def __init__(self, name, top_left_x, top_left_y, width, height):
		self.interface = Interface(name, top_left_x, top_left_y, width, height)

	def add_button(self, value, top_left_x, top_left_y):
		self.interface.add_child(value, top_left_x, top_left_y)

	def get_result(self):
		return self.interface

class SingleButtonInterfaceDirector:
	
	@staticmethod
	def construct(name, top_left_x, top_left_y, width, height, button_x, button_y, button_width, button_height):
		guibuilder = GUIBuilder(name, top_left_x, top_left_y, width, height)

		new_button = Button(button_x, button_y, button_width, button_height)

		return guibuilder.add_button(new_button).get_result()