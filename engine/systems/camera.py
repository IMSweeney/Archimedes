from engine import system
from engine import event
from engine import entity_component

from engine.entity_component import Position, Vector2D

from engine import logger
_logger = logger.Logger(__name__)


class CameraManager(system.System):
    def __init__(self, event_manager):
        super().__init__(
            set(['UpdateEvent']),
            set([Camera, Position])
        )
        self.event_manager = event_manager
        self.last_position = Vector2D(0, 0)

    def process(self, e):
        for guid, components in self.entities.items():
            position = components['Position'].position
            if position != self.last_position:
                self.last_position = position
                e = CameraMoveEvent(position)
                self.event_manager.push_event(e)


class CameraMoveEvent(event.Event):
    def __init__(self, position):
        self.type = self.__class__.__name__
        self.position = position


class Camera(entity_component.Component):
    def __init__(self):
        pass
