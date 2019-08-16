from human import Human, Finger
from model_util import EventHandler
from environment import TestEnvironmentDirector

def main():
    #Environment in which the interaction is situated
    environment = TestEnvironmentDirector.construct(500,500)

    human = TestHumanDirector.construct()

    device = TestTouchScreenDeviceDirector.construct()

    interface = SingleButtonInterfaceDirector.construct()

    device.children["touch_screen"].add_child(interface, 0, 0)

    # environment.add_human(human, loc_x, loc_y)
    environment.children["plane_1"].add_child(device, 50, 100)

    human.body_parts["eyes"].handler = environment.children["plane_1"]
    human.body_parts["right_hand_index"].handler = environment.children["plane_1"]

    human.execute_intent("point_at_button")
    # environment = Plane(0, 0, 500, 500)
    # finger = Finger(0, 0, environment)
    # human = Human()

