from engine import system
from engine import event

import pygame
import pygame.locals

from engine import logger
_logger = logger.Logger(__name__)


class InputHandler(system.System):
    def __init__(self, event_manager):
        super().__init__(set(['UpdateEvent']), set())
        pygame.init()
        self.event_manager = event_manager

    def process(self, e):
        for pygame_event in pygame.event.get():
            if pygame_event.type == pygame.locals.QUIT:
                e = WindowQuitEvent()
                self.event_manager.push_event(e)

            elif pygame_event.type == pygame.locals.KEYDOWN:
                e = KeyDownEvent(
                    pygame_event.key,
                    pygame_event.mod)
                _logger.info(e)
                self.event_manager.push_event(e)

            elif pygame_event.type == pygame.locals.KEYUP:
                e = KeyUpEvent(
                    pygame_event.key,
                    pygame_event.mod)
                self.event_manager.push_event(e)


class KeyEvent(event.Event):
    def __init__(self, key_code, mod):
        self.type = self.__class__.__name__
        self.key_code = key_code
        self.mod = mod


class KeyUpEvent(KeyEvent):
    def __init__(self, key_code, mod):
        super().__init__(key_code, mod)


class KeyDownEvent(KeyEvent):
    def __init__(self, key_code, mod):
        super().__init__(key_code, mod)


class WindowQuitEvent(event.Event):
    def __init__(self, event_info={}):
        self.type = self.__class__.__name__
        self.info = event_info


if __name__ == '__main__':
    pass
