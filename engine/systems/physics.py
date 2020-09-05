from engine import system
from engine.components.components import *
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
        for guid in self.entities:
            ll, ur = self.ll_ur_from_guid(guid)
            self.hash.add_obj_by_box(guid, ll, ur)

    def get_collisions(self, entityid):
        if entityid not in self.entities:
            _logger.error('Entity {} not tracked'.format(entityid))

        ll, ur = self.ll_ur_from_guid(entityid)

        possible_collisions = self.get_possible_collisions(entityid)
        for guid in possible_collisions:
            if guid == entityid:
                continue
            llo, uro = self.ll_ur_from_guid(guid)
            if ((ll.x < uro.x and ur.x > llo.x) and
                    (ll.y < uro.y and ur.y > llo.y)):
                return True
        return False

    def get_possible_collisions(self, entityid):
        ll, ur = self.ll_ur_from_guid(entityid)
        return self.hash.get_objs_from_bounds(ll, ur)

    def ll_ur_from_guid(self, entityid):
        pos = self.entities[entityid]['Position'].position
        box = self.entities[entityid]['CollisionBox']
        ll = pos + box.ll_bound
        ur = pos + box.ur_bound
        return ll, ur


class PhysicsHandler(system.System):
    def __init__(self):
        super().__init__(
            set(['UpdateEvent']),
            set([Position, Physics])
        )
        self.collision_handler = CollisionHandler(2)
        self.add_subsystem(self.collision_handler)

    def process(self, e):
        if e.type == 'UpdateEvent':
            self.collision_handler.regenerate_hash()
            for guid, components in self.entities.items():
                self.update_vel(components, e.dt / 1000)
                self.update_pos(guid, components, e.dt / 1000)

    def update_vel(self, entity, dt):
        physics = entity['Physics']
        d = physics.damping
        physics.velocity -= (physics.velocity * d * dt)

        total_force = Vector2D(0, 0)
        for force in physics.applied_forces.values():
            total_force += force
        physics.total_force = total_force
        physics.velocity += (total_force * dt)
        # entity['Physics'].velocity += (entity['Physics'].applied_forces * dt)

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


if __name__ == '__main__':
    pass
