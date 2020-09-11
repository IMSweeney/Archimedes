from engine.system import System

from engine import logger
_logger = logger.Logger(__name__)

import pygame_gui as pgui
import pygame


class UIFactory():
    def __init__(self):
        self.manager = PGManager.Instance().manager

        self.default_rect = pygame.Rect(0, 0, 80, 20)

    def create_element(self, details):
        e = pgui.elements.ui_label.UILabel(
            text=details['text'],
            relative_rect=self.default_rect,
            manager=self.manager)
        return e


class UIManager(System):
    def __init__(self):
        events = [
            'UpdateEvent',
            'WindowResizeEvent',
            'KeyDownEvent',
            'KeyUpEvent',
            'MouseButtonEvent',
            'MouseMotionEvent',
            'UserEvent',
        ]
        super().__init__(
            set(events),
            set()
        )

        self.manager = PGManager.Instance().manager

    def process(self, e):
        if e.type == 'UpdateEvent':
            self.manager.update(e.dt / 1000)
        elif e.type == 'WindowResizeEvent':
            self.win_size = e.size
        else:
            self.manager.process_events(e.pge)


class UIRenderer(System):
    def __init__(self, window):
        super().__init__(
            set(),
            set()
        )

        self.manager = PGManager.Instance().manager
        self.window = window

    def process(self, e):
        pass

    def render(self):
        self.manager.draw_ui(self.window)


# Source:
#   https://medium.com/better-programming/singleton-in-python-5eaa66618e3d
# Autor:
#   Goutom Roy
class Singleton:
    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


@Singleton
class PGManager():
    def __init__(self):
        self.manager = pgui.UIManager((200, 200))


if __name__ == '__main__':
    pass
