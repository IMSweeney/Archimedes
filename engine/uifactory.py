from engine.systems.ui_renderer import UITransform, UIConstraints
from engine.entity_component import Visual, Vector2D

import pygame


class UIGenerator():
    def __init__(self, arch_manager):
        self.arch_manager = arch_manager
        alpha = 255
        self.bg_color = (50, 230, 210, alpha)

    def generate_ui_elements(self):
        size = (100, 100)
        surface = pygame.Surface(size).convert()
        surface.fill(self.bg_color)
        e = self.arch_manager.add_entity()
        components = [
            Visual(surface),
            UITransform(),
            UIConstraints(relative_pos=Vector2D(1, 1),
                          relative_size=Vector2D(.6, .6))
        ]
        for component in components:
            self.arch_manager.attach_component(e, component)

    def ui_button():
        pass


if __name__ == '__main__':
    pass
