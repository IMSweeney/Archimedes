from engine import system
from engine.systems.world_renderer import WorldRenderer
from engine.systems.ui_renderer import UIRenderer

import pygame
import pygame.locals

from engine import logger
_logger = logger.Logger(__name__)


class RootRenderer(system.System):
    def __init__(self, event_manager):
        super().__init__(
            set(['UpdateEvent', 'WindowQuitEvent', 'WindowResizeEvent']),
            set()
        )
        self.event_manager = event_manager
        pygame.init()
        self.win_size = (640, 640)
        self.window = pygame.display.set_mode(
            self.win_size, flags=pygame.RESIZABLE
        )
        self.window.fill((250, 250, 250))

        self.add_subsystem(WorldRenderer(self.window))
        self.add_subsystem(UIRenderer(self.window))

    def process(self, e):
        if e.type == 'WindowQuitEvent':
            exit()
        elif e.type == 'UpdateEvent':
            self.render()
        elif e.type == 'WindowResizeEvent':
            self.win_size = e.size

    def render(self):
        for sys in self.subsystems:
            sys.render()
        pygame.display.flip()


if __name__ == '__main__':
    pass
