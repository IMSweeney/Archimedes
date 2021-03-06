from engine import system
from engine.components.components import *

from engine import logger
_logger = logger.Logger(__name__)


import pygame


class TetherSystem(system.System):
    def __init__(self, arch_manager, world_generator):
        super().__init__(
            set(['UpdateEvent']),
            set([Tether])
        )
        self.arch_manager = arch_manager
        self.ec_manager = arch_manager.ec_manager
        self.world_generator = world_generator
        self.tile_size = world_generator.tile_size

        self.add_subsystem(
            TetherAnchorSystem(
                arch_manager, world_generator))

    def process(self, e):
        if e.type == 'UpdateEvent':
            for guid, entity in self.entities.items():
                self.process_entity(entity)
                if 'Visual' in entity:
                    self.update_visual(entity)

    def process_entity(self, entity):
        half_tile = Vector2D(.5, -.5)
        tether = entity['Tether']

        # Get head and tail entities
        head = None
        tail = None
        if not isinstance(tether.head, Vector2D):
            head = self.ec_manager.get_entity(tether.head)
        if not isinstance(tether.tail, Vector2D):
            tail = self.ec_manager.get_entity(tether.tail)

        # Get world positions for head and tail
        if head:
            head_pos = head['Position'].position + half_tile
        else:
            head_pos = tether.head + half_tile

        if tail:
            tail_pos = tail['Position'].position + half_tile
        else:
            tail_pos = tether.tail + half_tile
        tether.vect = head_pos - tail_pos

        if head:
            self.restrain_head_with_force(tether, head)
        if tail:
            self.restrain_tail_with_force(tether, tail)

        self.update_sprite_pos(entity, head_pos, tail_pos)
        pass

    def restrain_head_with_force(self, tether, head):
        if not tether.max_length or 'Physics' not in head:
            return

        mag, ang = tether.vect.to_polar()
        overshoot = mag - tether.max_length
        if overshoot > 0:
            tether.stretched = True
            # Spring force in tether direction
            spring_force = -1 * tether.k * overshoot
            spring_force *= (tether.vect * (1 / mag))
            head['Physics'].applied_forces['Tether'] = spring_force
        else:
            tether.stretched = False
            try:
                head['Physics'].applied_forces.pop('Tether')
            except KeyError:
                return

    def restrain_tail_with_force(self, tether, tail):
        if not tether.max_length or 'Physics' not in tail:
            return

        mag, ang = tether.vect.to_polar()
        overshoot = mag - tether.max_length
        if overshoot > 0:
            tether.stretched = True
            # Spring force in tether direction
            spring_force = -1 * tether.k * overshoot
            spring_force *= (tether.vect * (1 / mag))
            tail['Physics'].applied_forces['Tether'] = -1 * spring_force
        else:
            tether.stretched = False
            try:
                tail['Physics'].applied_forces.pop('Tether')
            except KeyError:
                return

    def restrain_head_with_velocity(self, tether, head):
        mag, ang = tether.vect.to_polar()
        if (tether.max_length and mag > tether.max_length
                and head and 'Physics' in head):
            vel = head['Physics'].velocity
            dot = vel.dot(tether.vect)
            # Is it moving away
            if dot < 0:
                pass
            else:
                # Projection of force in tether direction
                proj = (dot / (mag ** 2)) * tether.vect
                _logger.info((vel, proj))
                head['Physics'].velocity -= proj

    def restrain_head_with_position(self, tether, head, tail_pos):
        mag, ang = tether.vect.to_polar()
        if (tether.max_length and mag > tether.max_length and head):
            max_tether = (tether.max_length / mag) * tether.vect
            head['Position'].position = tail_pos - max_tether

    def update_sprite_pos(self, entity, head_pos, tail_pos):
        entity['Position'].position.x = min(head_pos.x, tail_pos.x)
        entity['Position'].position.y = max(head_pos.y, tail_pos.y)

    def update_visual(self, entity):
        visual = entity['Visual']
        tether = entity['Tether']
        mag, ang = tether.vect.to_polar()

        if tether.stretched:
            tether.surface.fill(pygame.Color('red'))
        else:
            tether.surface.fill(pygame.Color('black'))

        # px_thickness = min(int(tether.thickness * self.tile_size), 4)
        # scaled = pygame.transform.smoothscale(
        #     tether.surface, (int(mag * self.tile_size), px_thickness))
        visual.surface = pygame.transform.rotate(
            tether.surface, ang).convert_alpha()


class TetherAnchorSystem(system.System):
    def __init__(self, arch_manager, world_generator):
        super().__init__(
            set(['UpdateEvent']),
            set([TetherAnchor]),
        )

        self.arch_manager = arch_manager
        self.ec_manager = arch_manager.ec_manager
        self.world_generator = world_generator
        self.tile_size = world_generator.tile_size

    def process(self, e):
        if e.type == 'UpdateEvent':
            for guid, entity in self.entities.items():
                self.process_entity(guid, entity)

    def process_entity(self, guid, entity):
        anchor = entity['TetherAnchor']
        if not anchor.tether:
            _logger.warning('Anchor with no cable: {}'.format(guid))
            return

        tether = self.ec_manager.get_entity(anchor.tether)
        if tether['Tether'].stretched and anchor.stored_tethers > 0:
            self.prepend_tether(guid, anchor, tether['Tether'])

    def prepend_tether(self, anchor_id, anchor, tether):
        tether_uid = self.world_generator.create_tether()
        t = self.ec_manager.get_entity(tether_uid)
        new_tether = t['Tether']

        node_uid = self.world_generator.create_tether_node()
        n = self.ec_manager.get_entity(node_uid)

        # Add a tether at the base of anchor
        print('{}\n{}'.format(new_tether, tether))

        new_tether.tail = anchor_id
        new_tether.head = node_uid
        tether.tail = node_uid
        anchor.tether = tether_uid

        print('{}\n{}'.format(new_tether, tether))


if __name__ == '__main__':
    pass
