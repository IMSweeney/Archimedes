from engine.systems.ui_renderer import UITransform, UIConstraints
from engine.entity_component import Visual, Vector2D

from engine import logger
_logger = logger.Logger(__name__)

import pygame


class UIGenerator():
    def __init__(self, arch_manager):
        self.arch_manager = arch_manager
        alpha = 255
        self.bg_color = (50, 230, 210, alpha)

    def generate_ui_elements(self):
        e = self.generate_base_ui_element()
        self.child_ui_element(e)

    def generate_base_ui_element(self):
        size = (100, 100)
        surface = pygame.Surface(size).convert()
        surface.fill(self.bg_color)
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
                # relative_size=Vector2D(.2, .2),
            )
        ]
        for component in components:
            self.arch_manager.attach_component(e, component)


if __name__ == '__main__':
    pass
