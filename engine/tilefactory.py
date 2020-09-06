from engine.components.components import *

import pygame

import random
import os


class WorldGenerator():
    def __init__(self, arch_manager, tile_size=32):
        self.arch_manager = arch_manager
        self.tile_size = tile_size
        self.tiles = []

    def generate_random_map(self, map_size):
        BORDER = 2
        tiles = []
        max_x = int(map_size / 2)
        max_y = int(map_size / 2)
        for i in range(-1 * max_x, max_x + 1):
            for j in range(-1 * max_y, max_y + 1):
                if (i, j) == (0, 0):
                    t_type = 'ground'
                elif ((i - -1 * max_x <= BORDER or max_x - i <= BORDER) or
                      (j - -1 * max_y <= BORDER or max_y - j <= BORDER)):
                    t_type = 'water'
                else:
                    t_type = random.choices(
                        ['ground', 'water'], weights=(5, 1)
                    )[0]
                self.generate_tile((i, j), t_type)

        return tiles

    def generate_tile(self, location, tile_type):
        size = (self.tile_size, self.tile_size)
        surface = pygame.Surface(size).convert()
        color = {
            'ground': (0, 200, 0),
            'water': (0, 0, 200),
        }[tile_type]
        surface.fill(color)

        components = [
            Visual(surface),
            Position(location[0], location[1])
        ]
        if tile_type == 'water':
            components.append(CollisionBox())

        self.arch_manager.create_entity(components)

    def generate_player(self):
        size = (self.tile_size, self.tile_size)
        sprite_path = os.path.join('assets', 'sprites')
        sprite = os.path.join(sprite_path, 'Player.png')
        # sprite = r'assets\sprites\Player.png')
        surface = pygame.image.load(sprite).convert_alpha()
        surface = pygame.transform.smoothscale(surface, size)

        components = [
            Visual(surface),
            Camera(),
            Position(0, 0),
            Controlable(),
            Physics(),
            CollisionBox(size=0.6),
            Selectable(),
        ]
        return self.arch_manager.create_entity(components)

    def generate_tether(self, player):
        size = (self.tile_size, 4)
        surface = pygame.Surface(size).convert_alpha()
        components = [
            Visual(surface),
            Position(0, 0),
            Tether(
                surface=surface,
                max_length=5,
                head=player,
                tail=Vector2D(0, 0))
        ]
        return self.arch_manager.create_entity(components)


if __name__ == '__main__':
    pass
