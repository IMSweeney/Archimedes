from engine import system
from engine import entity_component
from engine.entity_component import Visual, Vector2D, Position

from engine import logger
_logger = logger.Logger(__name__)


class UIRenderer(system.System):
    def __init__(self, window):
        super().__init__(
            set(),
            set([UIPosition, Visual])
        )
        self.window = window

    def process(self, e):
        pass

    def render(self):
        for guid, components in self.entities.items():
            self.render_entity(components)

    def render_entity(self, entity):
        surface = entity['Visual'].surface
        px_pos = entity['UIPosition'].position.to_tuple()
        self.window.blit(surface, px_pos)


class UIPosition(Position):
    def __init__(self, x, y, parentid=None):
        super().__init__(x, y)
        self.parent = parentid


if __name__ == '__main__':
    pass
