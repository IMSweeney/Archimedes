from engine import system
from engine import entity_component
from engine.entity_component import Position, Vector2D
from engine.structures.spatial_hash import SpatialHash

from engine import logger
_logger = logger.Logger(__name__)


class CollisionHandler(system.System):
    def __init__(self):
        super().__init__(
            set(),
            set([Position, CollisionBox])
        )

    def get_collisions(self, entityid):
        if entityid not in self.entities:
            _logger.error('Entity {} not tracked'.format(entityid))

        pos = self.entities[entityid]['Position'].position
        box = self.entities[entityid]['CollisionBox']
        l, r, t, b = self.lrtb_from_pos_box(pos, box)
        # _logger.info([l, r, t, b])
        for guid, components in self.entities.items():
            if guid == entityid:
                continue
            pos = components['Position'].position
            box = components['CollisionBox']
            lo, ro, to, bo = self.lrtb_from_pos_box(pos, box)
            if l < ro and r > lo and b < to and t > bo:
                return True
        return False

    def lrtb_from_pos_box(self, position, box):
        left = (position + box.ll_bound).x
        right = (position + box.ur_bound).x
        top = (position + box.ur_bound).y
        bottom = (position + box.ll_bound).y
        return left, right, top, bottom


class PhysicsHandler(system.System):
    def __init__(self):
        super().__init__(
            set(['UpdateEvent']),
            set([Position, Physics])
        )
        # self.entities = SpatialHash()
        self.collision_handler = CollisionHandler()
        self.add_subsystem(self.collision_handler)

    def add_entity(self, entityid, components):
        self.entities[entityid] = {
            comp.__class__.__name__: comp for comp in components
        }

    def remove_entity(self, entityid):
        self.entities.pop(entityid)

    def process(self, e):
        if e.type == 'UpdateEvent':
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
        NUM_STEPS = 32
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
                break

        for i in range(NUM_STEPS):
            # Try y
            pos.y += (v.y * dt / NUM_STEPS)
            collisions = self.collision_handler.get_collisions(guid)
            if collisions:
                pos.y = old_y
                break


class Physics(entity_component.Component):
    def __init__(self, damping=20):
        self.damping = damping
        self.velocity = Vector2D(0, 0)
        self.applied_forces = Vector2D(0, 0)


class CollisionBox(entity_component.Component):
    def __init__(self, size=1):
        self.ll_bound = Vector2D(-size / 2, -size / 2)
        self.ur_bound = Vector2D(size / 2, size / 2)
        self.center = Vector2D(0, 0)


if __name__ == '__main__':
    pass
