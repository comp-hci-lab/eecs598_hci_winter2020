from model_util import EventHandler
from abc import ABCMeta, abstractmethod
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Interface(EventHandler):

    def __init__(self, name, label, top_left_x, top_left_y, width, height):
        super(Interface, self).__init__(name, label,top_left_x, top_left_y, width, height)

class Input_Widget(Interface):

    def __init__(self, name, label,top_left_x, top_left_y, width, height):
        super(Input_Widget, self).__init__(name, label,top_left_x, top_left_y, width, height)


class Output_Widget(Interface):

    def __init__(self, name, label, top_left_x, top_left_y, width, height):
        super(Output_Widget, self).__init__(name, label,top_left_x, top_left_y, width, height)


class Button(Input_Widget):
	def __init__(self, name, label, top_left_x, top_left_y, width, height):
		super(Button, self).__init__(name, label, top_left_x, top_left_y, width, height)
		self.state = False
	
	def handle(self, event):
		return self.accept(event.body_part)

	def accept(self, body_part):
		return body_part.visitButton(self)

	
	def press(self):
		'''Change state of device to pressed, if successful'''
		self.state = True

	def draw(self, ax, origin_x=0, origin_y=0):
		''' In addition to rectangle it draws character text. '''
		super().draw(ax, origin_x, origin_y)

		label_x = origin_x + self.top_left_x + self.width/2
		label_y = origin_y + self.top_left_y + self.height/2

		ax.annotate(self.name, (label_x, label_y), color='b', weight='bold', fontsize=6, ha='center', va='center')