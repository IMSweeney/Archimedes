from engine import logger
_logger = logger.Logger(__name__)

import queue


class EventManager():
    def __init__(self):
        self.events = queue.Queue()

    def push_event(self, event):
        self.events.put(event)

    def pop_event(self):
        return self.events.get()

    def get_events(self):
        while not self.events.empty():
            yield self.pop_event()


class Event():
    def __init__(self):
        pass

    def __repr__(self):
        return '{} - {}'.format(self.type, self.__dict__)


class ComponentAttachedEvent(Event):
    def __init__(self, entityid, component):
        self.type = self.__class__.__name__
        self.component = component
        self.entityid = entityid


class UpdateEvent(Event):
    def __init__(self, dt):
        self.type = self.__class__.__name__
        self.dt = dt


class EntityCreateEvent(Event):
    def __init__(self, entity_id):
        self.type = self.__class__.__name__
        self.id = entity_id


class EntityDestroyEvent(Event):
    def __init__(self, entity_id):
        self.type = self.__class__.__name__
        self.id = entity_id
