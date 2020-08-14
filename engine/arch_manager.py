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

    def add_entity(self):
        eid = self.ec_manager.create_entity()
        return eid

    def attach_component(self, entid, comp):
        components = self.ec_manager.attach_component(entid, comp)
        self.system_manager.add_entity_to_systems(entid, components)

    def add_systems(self, systems):
        for sys in systems:
            self.add_system(sys)

    def add_system(self, sys):
        self.system_manager.add_system(sys)
        self.add_entities_to_system(sys)

    def add_entities_to_system(self, sys):
        entities = self.ec_manager.get_entities_with_component_set(sys.component_types)
        for guid, components in entities.items():
            sys.add_entity(guid, components)

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
                sys.process(e)


if __name__ == '__main__':
    pass
