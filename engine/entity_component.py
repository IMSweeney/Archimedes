import pandas as pd

from engine import logger
_logger = logger.Logger(__name__)


class EntityComponentManager():
    def __init__(self):
        self.entity_manager = EntityManager()
        self.component_types = set()
        self.database = pd.DataFrame(columns=['alive'])

    def create_entity(self):
        eid = self.entity_manager.create_entity()
        # _logger.info('entity {} created'.format(eid))
        if self.does_entity_exist(eid):
            raise ValueError('Entity already active')

        self.database.loc[eid, 'alive'] = True
        return eid

    def attach_component(self, entityid, component):
        if not self.does_entity_exist(entityid):
            raise IndexError('entity {} does not exist'.format(entityid))

        component_type = component.__class__.__name__
        if component_type not in self.component_types:
            self.add_component_type(component_type)

        self.database.loc[entityid, component_type] = component
        # _logger.info('{} component attached to entity {}'.format(
        #     component_type, entityid))
        return self.database.loc[entityid]

    def does_entity_exist(self, eid):
        return eid in self.database.index

    def add_component_type(self, component_type):
        self.component_types.add(component_type)
        self.database.insert(0, component_type, None)

    def get_entities_with_component_set(self, component_set):
        try:
            entities = self.database[list(component_set)]
            entities = entities.dropna(how='any')
            return entities
        except KeyError:  # if none of the components have an entity
            return {}

    # def get_entity_components_from_ids(self, ids):
    #     return self.database.loc[ids].to_dict(orient='records')


class EntityManager():
    def __init__(self):
        self.guid = 0

    def create_entity(self):
        self.guid += 1
        return self.guid


class Component():
    def __init__(self):
        raise NotImplementedError()


class Vector2D(Component):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self, asint=False):
        if not asint:
            return (self.x, self.y)
        else:
            return (int(self.x), int(self.y))

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        else:
            return Vector2D(self.x * other, self.y * other)

    def __rmul__(self, other):
        self.__mul__(other)

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __gt__(self, other):
        return self.x > other.x or self.y > other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '({:.2f}, {:.2f})'.format(self.x, self.y)


class Position(Component):
    def __init__(self, x, y):
        self.position = Vector2D(x, y)


class Visual(Component):
    def __init__(self, surface):
        self.surface = surface
