from engine import system
from engine.components.components import *

from engine import logger
_logger = logger.Logger(__name__)

from pygame.locals import KMOD_CTRL


class ScrollSystem(system.System):
    def __init__(self, ec_manager):
        super().__init__(
            set(['MouseButtonEvent', 'UpdateEvent']),
            set([UITransform, Scrollable])
        )
        self.ec_manager = ec_manager
        self.SCROLL_FORCE = 10

    def process(self, e):
        if e.type == 'MouseButtonEvent':
            for entity, components in self.entities.items():
                if self.element_has_focus(e.pos, components['UITransform']):
                    self.scroll_entity(e, components)

        elif e.type == 'UpdateEvent':
            for entity, components in self.entities.items():
                pass

    def scroll_entity(self, event, entity):
        scroll_comp = entity['Scrollable']
        if event.mods & KMOD_CTRL:
            if event.button == 4:
                scroll_comp.position.x -= self.SCROLL_FORCE
            elif event.button == 5:
                scroll_comp.position.x += self.SCROLL_FORCE
        else:
            if event.button == 4:
                scroll_comp.position.y -= self.SCROLL_FORCE
            elif event.button == 5:
                scroll_comp.position.y += self.SCROLL_FORCE
        self.clamp_scroll(entity)

    def clamp_scroll(self, entity):
        scroll_pos = entity['Scrollable'].position
        text = entity['Text']
        parent = self.get_parent_transform(entity)

        max_scroll = text.size - parent.size
        scroll_pos.x = max(0, min(max(0, scroll_pos.x), max_scroll.x))
        scroll_pos.y = max(0, min(max(0, scroll_pos.y), max_scroll.y))

    def element_has_focus(self, mouse_pos, transform):
        mouse_pos = Vector2D(mouse_pos[0], mouse_pos[1])
        ul = transform.position
        lr = ul + transform.size
        is_gt_ul = mouse_pos.x > ul.x and mouse_pos.y > ul.y
        is_lt_lr = mouse_pos.x < lr.x and mouse_pos.y < lr.y
        return is_lt_lr and is_gt_ul

    def get_parent_transform(self, entity):
        pid = entity['UIConstraints'].parentid
        if pid:
            return self.ec_manager.get_entity(pid)['UITransform']
        else:
            return UITransform()


if __name__ == '__main__':
    pass
