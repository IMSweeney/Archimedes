from engine import system
from engine.components.components import *

from engine import logger
_logger = logger.Logger(__name__)

import queue


class FPSSystem(system.System):
    def __init__(self):
        super().__init__(
            set(['UpdateEvent']),
            set([FPSDisplay])
        )
        self.FPS_WINDOW = 60
        self.tick_lengths = queue.Queue(maxsize=self.FPS_WINDOW)

    def process(self, e):
        if e.type == 'UpdateEvent':
            self.update_fps(e.dt)

    def update_fps(self, dt):
        try:
            self.tick_lengths.put_nowait(dt)
        except queue.Full:
            fps = self.calculate_fps()
            for e in self.entities.values():
                e['Text'].text = fps
                e['Text'].dirty = True

    def calculate_fps(self):
        t = 0
        while not self.tick_lengths.empty():
            t += self.tick_lengths.get()
        return self.FPS_WINDOW / t * 1000


if __name__ == '__main__':
    pass
