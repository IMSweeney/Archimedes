from engine.components.components import *

import pygame

import random
import os


class WorldGenerator():
    def __init__(self, arch_manager, tile_size=32):
        self.arch_manager = arch_manager
        self.tile_size = tile_size
        self.tiles = []

        self.sprite_path = os.path.join('assets', 'sprites')

    def generate_random_map(self, map_size):
        BORDER = 2
        tiles = []
        max_x = int(map_size / 2)
        max_y = int(map_size / 2)
        for i in range(-1 * max_x, max_x + 1):
            for j in range(-1 * max_y, max_y + 1):
                if abs(i) < 1 or abs(j) < 1:
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
        sprite = os.path.join(self.sprite_path, 'Player.png')
        # sprite = r'assets\sprites\Player.png')
        surface = pygame.image.load(sprite).convert_alpha()
        surface = pygame.transform.smoothscale(surface, size)

        components = [
            Visual(surface),
            Camera(),
            Position(1, 0),
            Controlable(),
            Physics(),
            CollisionBox(size=0.6),
            Selectable(),
        ]
        return self.arch_manager.create_entity(components)

    def generate_tether_anchor(self, player):
        tether_id = self.create_tether()

        # Set the head of the tether to the player
        tether = self.arch_manager.ec_manager.get_entity(tether_id)
        tether['Tether'].head = player

        # Create Anchor
        size = (self.tile_size / 8,
                self.tile_size / 8)
        surface = pygame.Surface(size).convert()
        surface.fill((100, 100, 100))

        anchor = self.arch_manager.create_entity([
            Visual(surface),
            Position(0, 0),
            TetherAnchor(tether_id, stored_tethers=2),
            # Physics(mass=1000),
            # CollisionBox(size=0.2)
        ])

        # Set the tail of the tether to the anchor
        tether['Tether'].tail = anchor

        return anchor

    def create_tether(self):
        # Create Tether
        sprite = os.path.join(self.sprite_path, 'cable.png')
        surface = pygame.image.load(sprite).convert_alpha()

        tether_size = 0.5
        px_thickness = 2
        size = (
            int(self.tile_size * tether_size),
            px_thickness)
        surface = pygame.transform.smoothscale(surface, size)

        components = [
            Visual(surface),
            Position(0, 0),
            Tether(
                surface=surface,
                max_length=tether_size,
                head=None,
                tail=None),
        ]
        tether = self.arch_manager.create_entity(components)
        return tether

    def create_tether_node(self, position=Vector2D(0, 0)):
        components = [
            Position(position.x, position.y),
            Physics(),
            TetherNode(),
        ]
        uid = self.arch_manager.create_entity(components)
        return uid


if __name__ == '__main__':
    pass
