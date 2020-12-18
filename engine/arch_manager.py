from engine import entity_component
from engine import system
from engine import event
from engine import logger
_logger = logger.Logger(__name__)

from pygame.time import Clock


class ArchManager():
    def __init__(self):
        self.event_manager = event.EventManager()
        self.ec_manager = entity_component.EntityComponentManager()
        self.system_manager = system.SystemManager()

    def generate_new_entity_id(self):
        eid = self.ec_manager.create_entity()
        return eid

    def attach_components(self, entid, components):
        for comp in components:
            self.attach_component(entid, comp)

    def attach_component(self, entid, comp):
        components = self.ec_manager.attach_component(entid, comp)
        self.system_manager.add_entity_to_systems(entid, components)

    def create_entity(self, components):
        eid = self.generate_new_entity_id()
        for comp in components:
            self.attach_component(eid, comp)
        return eid

    def add_systems(self, systems):
        for sys in systems:
            self.add_system(sys)

    def add_system(self, sys):
        self.system_manager.add_system(sys)
        self.add_entities_to_system(sys)
        for sub in sys.subsystems:
            self.add_system(sub)

    def add_entities_to_system(self, sys):
        entities = self.ec_manager.get_entities_with_component_set(
            sys.component_types)
        for guid, components in entities.items():
            components = [comp for k, comp in components.items()]
            sys.add_entity(guid, components)

    def remove_entity(self, entid):
        self.ec_manager.remove_entity(entid)
        self.system_manager.remove_entity(entid)

    def start(self, max_framerate=60):
        pg_clock = Clock()
        while True:
            dt = pg_clock.tick(max_framerate)
            self.run(dt)

    def run(self, dt):
        self.event_manager.push_event(
            event.UpdateEvent(dt))

        for e in self.event_manager.get_events():
            for sys in self.system_manager.get_listeners(e.type):
                _logger.debug('Processing {} with {}'.format(e, sys))
                sys.process(e)


if __name__ == '__main__':
    pass
