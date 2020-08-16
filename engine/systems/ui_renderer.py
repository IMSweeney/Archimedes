from engine import system
from engine import entity_component
from engine.entity_component import Visual, Vector2D, Position

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

    def process(self, e):
        if e.type == 'WindowResizeEvent':
            self.win_size = Vector2D(e.size[0], e.size[1])
            for eid, components in self.entities.items():
                components['UITransform'].dirty = True

    def render(self):
        for guid, components in self.entities.items():
            self.render_entity(components)

    def render_entity(self, entity):
        if entity['UITransform'].dirty:
            self.scale_element(entity)
            self.calculate_transform(entity)
            entity['UITransform'].dirty = False

        surface = entity['Visual'].surface
        px_pos = entity['UITransform'].position.to_tuple()
        self.window.blit(surface, px_pos)

    def calculate_transform(self, entity):
        constraints = entity['UIConstraints']
        transform = entity['UITransform']
        if not constraints.parentid:
            parent_pos = Vector2D(0, 0)
            parent_size = self.win_size
        else:
            parent = self.entities[constraints.parentid]
            parent_pos = parent['UITransform'].position
            parent_size = parent['UITransform'].size

        max_pos = parent_pos + parent_size - transform.size
        transform.position = (
            parent_pos + constraints.relative_pos * max_pos)

    def scale_element(self, entity):
        constraints = entity['UIConstraints']
        transform = entity['UITransform']
        visual = entity['Visual']
        if not constraints.parentid:
            parent_size = self.win_size
        else:
            parent = self.entities[constraints.parentid]
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
