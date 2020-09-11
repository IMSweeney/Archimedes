from engine.system import System

from engine import logger
_logger = logger.Logger(__name__)

import pygame_gui as pgui


class GUIManager(System):
    def __init__(self, win_size):
        super().__init__(
            set(['UpdateEvent', 'WindowResizeEvent']),
            set()
        )
        self.manager = pgui.UIManager(win_size)
        button = pgui.elements.UIButton(
            text='Hi!',
            manager=self.manager)

    def process(self, e):
        if e.type == 'UpdateEvent':
            self.manager.update(e.dt)
        else:
            self.manager.process_events(e.pge)


if __name__ == '__main__':
    pass
