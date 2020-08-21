from engine import system
from engine.components.components import *

from engine import logger
_logger = logger.Logger(__name__)


class UIInteraction(system.System):
    def __init__(self):
        super().__init__(
            set(['MouseButtonEvent']),
            set([UITransform, Selectable])
        )

    def process(self, e):
        if e.type == 'MouseButtonEvent':
            for entity, components in self.entities.items():
                if self.element_has_focus(e.pos, components['UITransform']):
                    self.process_entity(e, components)

    def process_entity(self, e, entity):
        if e.button == 1 and e.press:
            entity['Selectable'].state = not entity['Selectable'].state
            _logger.info(entity['Selectable'].state)

    def element_has_focus(self, mouse_pos, transform):
        mouse_pos = Vector2D(mouse_pos[0], mouse_pos[1])
        ul = transform.position
        lr = ul + transform.size
        is_gt_ul = mouse_pos.x > ul.x and mouse_pos.y > ul.y
        is_lt_lr = mouse_pos.x < lr.x and mouse_pos.y < lr.y
        return is_lt_lr and is_gt_ul


if __name__ == '__main__':
    pass
