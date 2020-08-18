from engine.entity_component import Visual, Vector2D
from engine.systems.ui_renderer import UITransform, UIConstraints
from engine.systems.ui_interaction import Clickable, Selectable
from engine.systems.text_renderer import Text

from engine import logger
_logger = logger.Logger(__name__)

import pygame


class UIGenerator():
    def __init__(self, arch_manager):
        self.arch_manager = arch_manager
        self.alpha = 100
        self.bg_color = (50, 230, 210)
        self.font = pygame.font.SysFont(None, 14)
        self.font_color = (0, 0, 0)

    def generate_ui_elements(self):
        e = self.generate_base_ui_element()
        self.child_ui_element(e)
        self.gen_fps_element()

    def generate_base_ui_element(self):
        size = (100, 100)
        surface = pygame.Surface(size).convert()
        surface.fill(self.bg_color)
        surface.set_alpha(self.alpha)
        e = self.arch_manager.add_entity()
        components = [
            Visual(surface),
            UITransform(),
            UIConstraints(relative_pos=Vector2D(1, 1),
                          relative_size=Vector2D(.2, .2))
        ]
        for component in components:
            self.arch_manager.attach_component(e, component)
        return e

    def child_ui_element(self, parentid):
        size = (100, 100)
        surface = pygame.Surface(size).convert()
        surface.fill((250, 250, 250))
        e = self.arch_manager.add_entity()
        components = [
            Visual(surface),
            UITransform(),
            UIConstraints(
                parentid=parentid,
                # relative_pos=Vector2D(.2, .2),
                relative_size=Vector2D(.2, .2),
            ),
            Selectable()
        ]
        for component in components:
            self.arch_manager.attach_component(e, component)

    def gen_fps_element(self):
        txt = 'FPS: '
        surface = self.font.render(txt, True, self.font_color)
        size = self.font.size(txt)
        e = self.arch_manager.add_entity()
        components = [
            Visual(surface),
            UITransform(size=size),
            UIConstraints(
                relative_pos=Vector2D(1, 0),
                # relative_size=Vector2D(.2, .2),
            ),
            Text(form='FPS: {:.0f}', txt=0),
        ]
        for component in components:
            self.arch_manager.attach_component(e, component)


if __name__ == '__main__':
    pass
