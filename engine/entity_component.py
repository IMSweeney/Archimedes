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
        if len(component_set) == 0:
            return {}
        try:
            entities = self.database[[comp.__name__ for comp in component_set]]
            entities = entities.dropna(how='any').index
            return self.get_eid_comps_from_ids(entities)
        except KeyError:  # if none of the components have an entity
            return {}

    def get_entities_with(self, component_set, extra=[]):
        if len(component_set) == 0:
            return self.database
        try:
            comp_names = [comp.__name__ for comp in component_set]
            entities = self.database.dropna(how='any', subset=comp_names)
            return entities[comp_names + extra]
        except KeyError:  # if none of the components have an entity
            return {}

    def get_eid_comps_from_ids(self, ids):
        return self.database.loc[ids].to_dict(orient='index')

    def get_entity(self, eid):
        e = self.database.loc[eid]
        e = e.dropna().to_dict()

        return EntityRepresentation(eid, e)

    def remove_entity(self, eid):
        self.database.drop(eid)


class EntityRepresentation():
    def __init__(self, eid, components):
        self.id = eid
        for k, v in components.items():
            self.__dict__[k] = v

    def __getitem__(self, key):
        return self.__dict__[key]

    def __contains__(self, item):
        return item in self.__dict__


class EntityManager():
    def __init__(self):
        self.guid = 0

    def create_entity(self):
        self.guid += 1
        return self.guid
