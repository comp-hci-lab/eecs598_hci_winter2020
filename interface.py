class Interface(EventHandler):

    def __init__(self, top_left_x, top_left_y, width, height):
        super().__init__(top_left_x, top_left_y, width, height)

class Input_Widget(Interface):

    def __init__(self, top_left_x, top_left_y, width, height):
        super().__init__(top_left_x, top_left_y, width, height)


class Output_Widget(Interface):

    def __init__(self, top_left_x, top_left_y, width, height):
        super().__init__(top_left_x, top_left_y, width, height)



class Button(Input_Widget):

    def __init__(self, top_left_x, top_left_y, width, height):
		super().__init__(top_left_x, top_left_y, width, height)
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