from engine import system
from engine import event

import pygame
from pygame.locals import *

from engine import logger
_logger = logger.Logger(__name__)


class InputHandler(system.System):
    def __init__(self, event_manager):
        super().__init__(set(['UpdateEvent']), set())
        pygame.init()
        self.event_manager = event_manager

    def process(self, e):
        for pygame_event in pygame.event.get():
            if pygame_event.type == QUIT:
                e = WindowQuitEvent()
                self.event_manager.push_event(e)

            elif pygame_event.type == KEYDOWN:
                e = KeyDownEvent(
                    pygame_event.key,
                    pygame_event.mod)
                _logger.info(e)
                self.event_manager.push_event(e)

            elif pygame_event.type == KEYUP:
                e = KeyUpEvent(
                    pygame_event.key,
                    pygame_event.mod)
                self.event_manager.push_event(e)

            elif pygame_event.type == VIDEORESIZE:
                e = WindowResizeEvent(pygame_event.size)
                self.event_manager.push_event(e)
                _logger.info(e)

            elif pygame_event.type in [MOUSEBUTTONDOWN,
                                       MOUSEBUTTONUP]:
                e = MouseButtonEvent(
                    pygame_event.pos,
                    pygame_event.button,
                    pygame_event.type == MOUSEBUTTONDOWN,
                    mods=pygame.key.get_mods()
                )
                self.event_manager.push_event(e)
                # _logger.info(e)

            elif pygame_event.type in [MOUSEMOTION]:
                e = MouseMotionEvent(
                    pygame_event.pos,
                )
                self.event_manager.push_event(e)
                # _logger.info(e)


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


class WindowResizeEvent(event.Event):
    def __init__(self, size):
        self.type = self.__class__.__name__
        self.size = size


class MouseButtonEvent(event.Event):
    def __init__(self, pos, button, press, mods=0):
        self.type = self.__class__.__name__
        self.pos = pos
        self.button = button
        self.press = press
        self.mods = mods


class MouseMotionEvent(event.Event):
    def __init__(self, pos):
        self.type = self.__class__.__name__
        self.pos = pos


if __name__ == '__main__':
    pass
