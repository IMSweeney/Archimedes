from engine import system
from engine.components.components import *

from engine import logger
_logger = logger.Logger(__name__)


class HoverSystem(system.System):
    def __init__(self):
        super().__init__(
            set(['MouseMotionEvent', 'UpdateEvent']),
            set([UITransform, Hoverable])
        )

    def process(self, e):
        if e.type == 'MouseMotionEvent':
            for entity, components in self.entities.items():
                if self.element_has_focus(e.pos, components['UITransform']):
                    components['Hoverable'].is_hovered = True
                    components['Hoverable'].timer = 0
                else:
                    components['Hoverable'].is_hovered = False
                    components['Hoverable'].timer = 0

        if e.type == 'UpdateEvent':
            for entity, components in self.entities.items():
                self.update_hover_timer(e.dt / 1000, components)

    def update_hover_timer(self, dt, entity):
        hover_comp = entity['Hoverable']
        if hover_comp.state and not hover_comp.is_hovered:
            hover_comp.timer += dt
            if hover_comp.timer > hover_comp.off_delay:
                hover_comp.timer = 0
                hover_comp.state = False
                _logger.info('Unhovered')

        elif hover_comp.is_hovered and not hover_comp.state:
            hover_comp.timer += dt
            if hover_comp.timer > hover_comp.on_delay:
                hover_comp.timer = 0
                hover_comp.state = True
                _logger.info('hovered')

    def element_has_focus(self, mouse_pos, transform):
        mouse_pos = Vector2D(mouse_pos[0], mouse_pos[1])
        ul = transform.position
        lr = ul + transform.size
        is_gt_ul = mouse_pos.x > ul.x and mouse_pos.y > ul.y
        is_lt_lr = mouse_pos.x < lr.x and mouse_pos.y < lr.y
        return is_lt_lr and is_gt_ul


if __name__ == '__main__':
    pass
