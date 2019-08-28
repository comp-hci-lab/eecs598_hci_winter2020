from human import TestHumanBuilderDirector, StandardBodyPartFactory
from device import TouchScreenDeviceDirector
from model_util import EventHandler
from abc import ABCMeta, abstractmethod

class Plane(EventHandler):
    
    def __init__(self, name, top_left_x, top_left_y, width, height):
        super().__init__(name, top_left_x, top_left_y, width, height)

class PlaneBuilder:
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_size(self, x, y, width, height):
        pass

    @abstractmethod
    def set_name(self, value):
        pass

    @abstractmethod
    def set_device(self, value):
        pass

    @abstractmethod
    def get_result(self):
        pass

class SimplePlaneBuilder(PlaneBuilder):
    def __init__(self):
        self.plane = Plane("simple_plane", 0,0,0,0)
    
    def set_size(self, x, y, width, height):
        self.plane.top_left_x = x
        self.plane.top_left_y = y
        self.plane.width = width
        self.plane.height = height      
        return self

    def set_name(self, value):
        self.plane.name = value
        return self

    def set_device(self, value):
        '''Setting to default locations'''
        self.plane.add_child(value, 0, 0)
        return self

    def get_result(self):
        return self.plane


class TestSimplePlaneBuilderDirector:
    @staticmethod
    def construct(x, y, width, height):
        device = TouchScreenDeviceDirector().construct(width/2, height/2, 25, 50)
        return SimplePlaneBuilder().set_size(x, y, width, height).set_device(device).get_result()

class Environment(EventHandler):
    
    def __init__(self, top_left_x, top_left_y, width, height):
        super().__init__(top_left_x, top_left_y, width, height)
        self.humans = []


class EnvironmentBuilder:
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_human(self, value):
        pass

    @abstractmethod
    def set_plane(self, value):
        pass

    @abstractmethod
    def get_result(self):
        pass

class SinglePlaneEnvironmentBuilder(EnvironmentBuilder):
    
    def __init__(self, width, height):
        self.environment = Environment(0,0,width,height)

    def set_human(self, value):
        self.environment.humans.append(value)
        return self

    def set_plane(self, value):
        '''Setting to default locations'''
        self.environment.add_child(value, 0, 0)
        return self
    
    def get_result(self):
        return self.environment


class TestEnvironmentDirector:
    @staticmethod
    def construct(environment_width, environment_height):
        body_part_factory = StandardBodyPartFactory()
        environment_builder = SinglePlaneEnvironmentBuilder(environment_width,environment_height)
        return environment_builder.set_human(TestHumanBuilderDirector.construct(body_part_factory, environment_builder.environment)).set_plane(TestSimplePlaneBuilderDirector.construct(0, 0, environment_width, environment_height)).get_result()

