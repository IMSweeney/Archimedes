from engine import system
from engine.components.components import *

from engine import logger
_logger = logger.Logger(__name__)


import pygame


class TetherSystem(system.System):
    def __init__(self, arch_manager, tile_size):
        super().__init__(
            set(['UpdateEvent']),
            set([Tether])
        )
        self.arch_manager = arch_manager
        self.ec_manager = arch_manager.ec_manager
        self.tile_size = tile_size

    def process(self, e):
        if e.type == 'UpdateEvent':
            for guid, entity in self.entities.items():
                self.process_entity(entity)
                if 'Visual' in entity:
                    self.update_visual(entity)

    def process_entity(self, entity):
        half_tile = Vector2D(.5, -.5)
        tether = entity['Tether']
        head = None
        tail = None
        if not isinstance(tether.head, Vector2D):
            head = self.ec_manager.get_entity(tether.head)
        if not isinstance(tether.tail, Vector2D):
            tail = self.ec_manager.get_entity(tether.tail)

        if head:
            head_pos = head['Position'].position + half_tile
        else:
            head_pos = tether.head + half_tile

        if tail:
            tail_pos = tail['Position'].position + half_tile
        else:
            tail_pos = tether.tail + half_tile
        tether.vect = head_pos - tail_pos
        self.update_sprite_pos(entity, head_pos, tail_pos)
        pass

    def update_sprite_pos(self, entity, head_pos, tail_pos):
        entity['Position'].position.x = min(head_pos.x, tail_pos.x)
        entity['Position'].position.y = max(head_pos.y, tail_pos.y)

    def update_visual(self, entity):
        visual = entity['Visual']
        tether = entity['Tether']
        mag, ang = tether.vect.to_polar()
        _logger.info([mag, ang])

        scaled = pygame.transform.smoothscale(
            tether.surface, (int(mag * self.tile_size), 4))
        visual.surface = pygame.transform.rotate(
            scaled, ang).convert_alpha()


if __name__ == '__main__':
    pass