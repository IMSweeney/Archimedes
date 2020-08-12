from engine import system
from engine.entity_component import Visual, Position, Vector2D

import pygame
import pygame.locals

from engine import logger
_logger = logger.Logger(__name__)


class Renderer(system.System):
    def __init__(self, ec_manager, tile_size=32):
        super().__init__(
            set(['UpdateEvent', 'WindowQuitEvent', 'CameraMoveEvent']),
            set([Visual, Position])
        )
        pygame.init()
        self.win_size = (640, 640)
        self.tile_size = tile_size
        self.win_transform = Vector2D(
            self.win_size[0] / 2,
            self.win_size[1] / 2
        )
        self.window = pygame.display.set_mode(
            self.win_size, flags=pygame.RESIZABLE
        )
        self.window.fill((250, 250, 250))
        self.ec_manager = ec_manager
        self.camera_location = Vector2D(0, 0)

    def process(self, e):
        if e.type == 'WindowQuitEvent':
            exit()
        elif e.type == 'UpdateEvent':
            self.render_entities()
        elif e.type == 'CameraMoveEvent':
            self.move_camera(e)

    def move_camera(self, e):
        self.camera_location = e.position

    def render_entities(self):
        for guid, entity in self.entities.items():
            surface = entity['Visual'].surface
            position = entity['Position'].position
            px_pos = self.world_to_px_position(position)
            self.window.blit(surface, (px_pos.x, px_pos.y))

        pygame.display.flip()

    def world_to_px_position(self, world_pos):
        px_pos = (world_pos - self.camera_location) * self.tile_size
        px_pos.x += self.win_transform.x
        px_pos.y = self.win_transform.y - px_pos.y
        return px_pos


if __name__ == '__main__':
    pass
