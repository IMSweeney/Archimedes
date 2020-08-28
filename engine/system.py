from engine import logger
_logger = logger.Logger(__name__)


class SystemManager():
    def __init__(self):
        self.systems = []
        self.event_listeners = {}

    def add_system(self, system):
        _logger.info('System added: {}'.format(system))
        for event_type in system.event_types:
            self.add_event_listener(event_type, system)
        self.systems.append(system)

    def add_event_listener(self, event_type, system):
        if event_type not in self.event_listeners:
            self.event_listeners[event_type] = []
        self.event_listeners[event_type].append(system)

    def remove_system(self, system):
        for event_type in system.event_types:
            self.remove_event_listener(event_type, system)
        self.systems.remove(system)

    def remove_event_listener(self, event_type, system):
        self.event_listeners[event_type].remove(system)

    def get_listeners(self, event_type):
        if event_type in self.event_listeners:
            return self.event_listeners[event_type]
        else:
            _logger.warning('No watchers for event {}'.format(event_type))
            return []

    def add_entity_to_systems(self, entityid, components):
        component_types = set([comp.__class__ for comp in components])
        for system in self.systems:
            if len(system.component_types) == 0:
                continue
            if system.component_types.issubset(component_types):
                # _logger.info('adding entity {} to {}'.format(entityid, system))
                system.add_entity(entityid, components)


class System():
    def __init__(self, event_types, component_types):
        self.event_types = event_types
        self.component_types = component_types
        self.entities = {}
        self.subsystems = []

    def add_entity(self, entityid, components):
        self.entities[entityid] = {
            comp.__class__.__name__: comp for comp in components
        }

    def add_subsystem(self, subsystem):
        if not isinstance(subsystem, System):
            exit('{} is not a system'.format(subsystem))
        self.subsystems.append(subsystem)

    def remove_entity(self, entityid):
        self.entities.pop(entityid)

    def process(self, e):
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__
