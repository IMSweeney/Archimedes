from engine import system
from engine import entity_component
from engine.entity_component import Visual, Vector2D, Position
from engine.structures.tree import Tree

from engine import logger
_logger = logger.Logger(__name__)

import pygame


class UIRenderer(system.System):
    def __init__(self, window):
        super().__init__(
            set(['WindowResizeEvent']),
            set([UITransform, Visual, UIConstraints])
        )
        self.window = window
        size = window.get_size()
        self.win_size = Vector2D(size[0], size[1])
        self.entities = Tree()

    def add_entity(self, entityid, components):
        entity = {
            comp.__class__.__name__: comp for comp in components
        }
        parentid = components['UIConstraints'].parentid
        self.entities.add_element(entityid, entity, parentid=parentid)
        # _logger.info('added {}'.format(entityid))

    def remove_entity(self, entityid):
        self.entities.remove_element(entityid)

    def process(self, e):
        if e.type == 'WindowResizeEvent':
            self.win_size = Vector2D(e.size[0], e.size[1])
            for entity in self.entities:
                entity.data['UITransform'].dirty = True

    def render(self):
        for node in self.entities:
            self.render_entity(node.data, node)

    def render_entity(self, entity, node):
        if entity['UITransform'].dirty:
            self.scale_element(entity, node)
            self.calculate_transform(entity, node)
            entity['UITransform'].dirty = False

        surface = entity['Visual'].surface
        px_pos = entity['UITransform'].position.to_tuple()
        self.window.blit(surface, px_pos)

    def calculate_transform(self, entity, node):
        constraints = entity['UIConstraints']
        transform = entity['UITransform']
        if not node.parent:
            parent_pos = Vector2D(0, 0)
            parent_size = self.win_size
        else:
            parent = node.parent.data
            parent_pos = parent['UITransform'].position
            parent_size = parent['UITransform'].size

        max_pos = parent_pos + parent_size - transform.size
        transform.position = (
            parent_pos + constraints.relative_pos * max_pos)

    def scale_element(self, entity, node):
        constraints = entity['UIConstraints']
        transform = entity['UITransform']
        visual = entity['Visual']
        if not node.parent:
            parent_size = self.win_size
        else:
            parent = node.parent.data
            parent_size = parent['UITransform'].size

        size = constraints.relative_size * parent_size
        if size < constraints.minimum_size:
            raise InvalidResizeError()

        transform.size = size
        visual.surface = pygame.transform.scale(
            visual.surface, size.to_tuple(asint=True)
        )


class UITransform(Position):
    def __init__(self):
        super().__init__(0, 0)
        self.size = Vector2D(0, 0)
        self.dirty = True


class UIConstraints(entity_component.Component):
    def __init__(self, parentid=None,
                 relative_pos=Vector2D(0, 0),
                 relative_size=Vector2D(.2, .2),
                 minimum_size=Vector2D(0, 0)):
        self.parentid = parentid
        self.relative_pos = relative_pos
        self.relative_size = relative_size
        self.minimum_size = minimum_size


class InvalidResizeError(ValueError):
    pass


if __name__ == '__main__':
    pass
