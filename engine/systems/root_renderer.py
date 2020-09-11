from engine import system
from engine.systems.world_renderer import WorldRenderer
from engine.systems.ui_renderer import UIRenderer

from engine.gui import GUIManager

import pygame
import pygame.locals

from engine import logger
_logger = logger.Logger(__name__)


class RootRenderer(system.System):
    def __init__(self, arch_manager):
        super().__init__(
            set(['UpdateEvent', 'WindowQuitEvent', 'WindowResizeEvent']),
            set()
        )
        self.event_manager = arch_manager.event_manager
        self.ec_manager = arch_manager.ec_manager
        pygame.init()
        self.win_size = (800, 640)
        self.window = pygame.display.set_mode(
            self.win_size, flags=pygame.RESIZABLE
        )
        self.clear_surface()

        self.add_subsystem(WorldRenderer(self.window))
        # self.add_subsystem(UIRenderer(self.window, self.ec_manager))
        self.add_subsystem(GUIManager(self.window))

    def clear_surface(self):
        self.window.fill((0, 0, 0))

    def process(self, e):
        if e.type == 'WindowQuitEvent':
            exit()
        elif e.type == 'UpdateEvent':
            self.render()
        elif e.type == 'WindowResizeEvent':
            self.win_size = e.size

    def render(self):
        self.clear_surface()
        for sys in self.subsystems:
            sys.render()
        pygame.display.flip()


if __name__ == '__main__':
    pass
