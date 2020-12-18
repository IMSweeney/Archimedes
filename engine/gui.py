from engine.system import System

from engine import logger
_logger = logger.Logger(__name__)

import pygame_gui as pgui
import pygame

import queue
import matplotlib.pyplot as plt


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

        self.fps = pgui.elements.UIButton(
            relative_rect=pygame.Rect(0, 0, 100, 20),
            text='Hi!',
            manager=self.manager,
            anchors={
                'left': 'left',
                'right': 'left',
                'top': 'top',
                'bottom': 'top',
            })
        self.FPS_WINDOW = 60
        self.frame_lengths = queue.Queue(maxsize=self.FPS_WINDOW)

    def process(self, e):
        if e.type == 'UpdateEvent':
            self.manager.update(e.dt / 1000)
            self.update_fps(e.dt)
        elif e.type == 'WindowResizeEvent':
            self.win_size = e.size
        else:
            self.manager.process_events(e.pge)

    def update_fps(self, dt):
        try:
            self.frame_lengths.put_nowait(dt)
        except queue.Full:
            fps = self.calculate_fps()
            self.fps.set_text('{:.0f}'.format(fps))

    def calculate_fps(self):
        t = 0
        while not self.frame_lengths.empty():
            t += self.frame_lengths.get()
        return self.FPS_WINDOW / t * 1000


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
