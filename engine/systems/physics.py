from engine import system
from engine import entity_component
from engine.entity_component import Position, Vector2D
from engine.structures.spatial_hash import SpatialHash

from engine import logger
_logger = logger.Logger(__name__)


class CollisionHandler(system.System):
    def __init__(self, bin_size):
        super().__init__(
            set(),
            set([Position, CollisionBox])
        )
        self.hash = SpatialHash(bin_size)

    def regenerate_hash(self):
        self.hash.clear()
        for guid, components in self.entities.items():
            self.hash.add_obj(guid, components['Position'].position)

    def get_collisions(self, entityid):
        if entityid not in self.entities:
            _logger.error('Entity {} not tracked'.format(entityid))

        pos = self.entities[entityid]['Position'].position
        box = self.entities[entityid]['CollisionBox']
        l, r, t, b = self.lrtb_from_pos_box(pos, box)

        possible_collisions = self.get_possible_collisions(entityid)
        for guid in possible_collisions:
            if guid == entityid:
                continue
            components = self.entities[guid]
            pos = components['Position'].position
            box = components['CollisionBox']
            lo, ro, to, bo = self.lrtb_from_pos_box(pos, box)
            if l < ro and r > lo and b < to and t > bo:
                return True
        return False

    def get_possible_collisions(self, entityid):
        pos = self.entities[entityid]['Position'].position
        box = self.entities[entityid]['CollisionBox']
        return self.hash.get_objs_from_bounds(
            pos + box.ll_bound * 4,
            pos + box.ur_bound * 4
        )

    def lrtb_from_pos_box(self, position, box):
        ll = position + box.ll_bound
        ur = position + box.ur_bound
        return ll.x, ur.x, ur.y, ll.y


class PhysicsHandler(system.System):
    def __init__(self):
        super().__init__(
            set(['UpdateEvent']),
            set([Position, Physics])
        )
        self.collision_handler = CollisionHandler(4)
        self.add_subsystem(self.collision_handler)

    def process(self, e):
        if e.type == 'UpdateEvent':
            self.collision_handler.regenerate_hash()
            for guid, components in self.entities.items():
                self.update_vel(components, e.dt / 1000)
                self.update_pos(guid, components, e.dt / 1000)

    def update_vel(self, entity, dt):
        d = entity['Physics'].damping
        entity['Physics'].velocity -= (entity['Physics'].velocity * d * dt)
        entity['Physics'].velocity += (entity['Physics'].applied_forces * dt)
        # entity['Position'].position += (entity['Physics'].velocity * dt)
        # _logger.info(entity['Position'].position)

    def update_pos(self, guid, entity, dt):
        NUM_STEPS = 16
        pos = entity['Position'].position
        v = entity['Physics'].velocity

        old_x = pos.x
        old_y = pos.y

        for i in range(NUM_STEPS):
            # Try x
            pos.x += (v.x * dt / NUM_STEPS)
            collisions = self.collision_handler.get_collisions(guid)
            if collisions:
                pos.x = old_x
                v.x = 0
                break

        for i in range(NUM_STEPS):
            # Try y
            pos.y += (v.y * dt / NUM_STEPS)
            collisions = self.collision_handler.get_collisions(guid)
            if collisions:
                pos.y = old_y
                v.y = 0
                break


class Physics(entity_component.Component):
    def __init__(self, damping=10):
        self.damping = damping
        self.velocity = Vector2D(0, 0)
        self.applied_forces = Vector2D(0, 0)


class CollisionBox(entity_component.Component):
    def __init__(self, size=1):
        self.ll_bound = Vector2D(-size / 2, -size / 2)
        self.ur_bound = Vector2D(size / 2, size / 2)
        self.center = Vector2D(0, 0)

    def __repr__(self):
        return '{}, {}'.format(self.ll_bound, self.ur_bound)


if __name__ == '__main__':
    pass
