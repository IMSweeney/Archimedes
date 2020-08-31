from engine import system
from engine.components.components import *

from engine import logger
_logger = logger.Logger(__name__)

from pygame.locals import KMOD_CTRL


class UIInteraction(system.System):
    def __init__(self, ec_manager):
        super().__init__(
            set(),
            set()
        )
        self.ec_manager = ec_manager
        utils = UIInteractionUtils(ec_manager)

        self.add_subsystem(Hovering(utils))
        self.add_subsystem(Scrolling(utils))
        self.add_subsystem(Selecting(utils))

    def process(self, e):
        pass


class UIInteractionUtils():
    def __init__(self, ec_manager):
        self.ec_manager = ec_manager

    def element_has_focus(self, mouse_pos, transform):
        mouse_pos = Vector2D(mouse_pos[0], mouse_pos[1])
        ul = transform.position
        lr = ul + transform.size
        is_gt_ul = mouse_pos.x > ul.x and mouse_pos.y > ul.y
        is_lt_lr = mouse_pos.x < lr.x and mouse_pos.y < lr.y
        return is_lt_lr and is_gt_ul

    def get_parent_transform(self, entity):
        pid = entity['UITransform'].parentid
        if pid:
            return self.ec_manager.get_entity(pid)['UITransform']
        else:
            return UITransform()


class Selecting(system.System):
    def __init__(self, utils):
        super().__init__(
            set(['MouseButtonEvent']),
            set([UITransform, Selectable])
        )
        self.utils = utils

    def process(self, e):
        if e.type == 'MouseButtonEvent':
            for entity, components in self.entities.items():
                if self.utils.element_has_focus(e.pos, components['UITransform']):
                    self.process_entity(e, entity, components)

    def process_entity(self, e, guid, entity):
        if e.button == 1 and e.press:
            entity['Selectable'].state = not entity['Selectable'].state
            _logger.info('{:04d} -> {}'.format(
                guid, entity['Selectable'].state))


class Hovering(system.System):
    def __init__(self, utils):
        super().__init__(
            set(['MouseMotionEvent', 'UpdateEvent']),
            set([UITransform, Hoverable])
        )
        self.utils = utils

    def process(self, e):
        if e.type == 'MouseMotionEvent':
            for entity, components in self.entities.items():
                if self.utils.element_has_focus(e.pos, components['UITransform']):
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


class Scrolling(system.System):
    def __init__(self, utils):
        super().__init__(
            set(['MouseButtonEvent', 'UpdateEvent']),
            set([UITransform, Scrollable])
        )
        self.utils = utils
        self.SCROLL_FORCE = 10

    def process(self, e):
        if e.type == 'MouseButtonEvent':
            for entity, components in self.entities.items():
                if self.utils.element_has_focus(e.pos, components['UITransform']):
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
        entity['UITransform'].dirty = True

    def clamp_scroll(self, entity):
        scroll_pos = entity['Scrollable'].position
        size = entity['UITransform'].size
        parent = self.utils.get_parent_transform(entity)

        max_scroll = size - parent.size
        scroll_pos.x = max(0, min(max(0, scroll_pos.x), max_scroll.x))
        scroll_pos.y = max(0, min(max(0, scroll_pos.y), max_scroll.y))


if __name__ == '__main__':
    pass
