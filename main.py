from human import Human, Finger
from model_util import EventHandler
from environment import TestEnvironmentBuilderDirector

def main():
    #Environment in which the interaction is situated
    environment = TestEnvironmentBuilderDirector.construct(500,500,0,0,300,300)
    # environment = Plane(0, 0, 500, 500)
    # finger = Finger(0, 0, environment)
    # human = Human()

