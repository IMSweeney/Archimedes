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

    def get_entity_components_from_ids(self, ids):
        return self.database.loc[ids].to_dict(orient='records')

    def get_entity(self, eid):
        return self.database.loc[eid].to_dict(orient='records')


class EntityManager():
    def __init__(self):
        self.guid = 0

    def create_entity(self):
        self.guid += 1
        return self.guid
