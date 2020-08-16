from engine.systems.ui_renderer import UITransform, UIConstraints
from engine.entity_component import Visual

import pygame


class UIGenerator():
    def __init__(self, arch_manager):
        self.arch_manager = arch_manager

    def generate_ui_elements(self):
        size = (100, 100)
        surface = pygame.Surface(size).convert()
        e = self.arch_manager.add_entity()
        components = [
            Visual(surface),
            UITransform(160, 0),
            UIConstraints()
        ]
        for component in components:
            self.arch_manager.attach_component(e, component)


if __name__ == '__main__':
    pass
