from engine import system
from engine import entity_component
from engine.entity_component import Vector2D
from engine.ui_render import UITransform
from engine.structures.tree import Tree

from engine import logger
_logger = logger.Logger(__name__)


class UIRenderer(system.System):
    def __init__(self, window):
        super().__init__(
            set(['MouseButtonEvent']),
            set([UITransform])
        )
        self.entities = Tree()

    def add_entity(self, entityid, components):
        entity = {
            comp.__class__.__name__: comp for comp in components
        }
        parentid = components['UIConstraints'].parentid
        self.entities.add_element(entityid, entity, parentid=parentid)

    def remove_entity(self, entityid):
        self.entities.remove_element(entityid)

    def process(self, e):
        if e.type == 'WindowResizeEvent':
            self.win_size = Vector2D(e.size[0], e.size[1])
            for entity in self.entities:
                entity.data['UITransform'].dirty = True


class Clickable(entity_component.Component):
    def __init__(self):
        pass


class InvalidResizeError(ValueError):
    pass


if __name__ == '__main__':
    pass
