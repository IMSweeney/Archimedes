from engine import system
from engine import entity_component
from engine.entity_component import Vector2D, Visual

from engine import logger
_logger = logger.Logger(__name__)

import pygame

import queue


class TextRenderer(system.System):
    def __init__(self):
        super().__init__(
            set(['UpdateEvent']),
            set([Text, Visual])
        )
        self.fps_window = 10
        self.tick_lengths = queue.Queue(maxsize=self.fps_window)
        self.font = pygame.font.SysFont(None, 18)

    def process(self, e):
        if e.type == 'UpdateEvent':
            self.update_fps(e.dt)
            for guid, components in self.entities.items():
                self.render(components)

    def update_fps(self, dt):
        try:
            self.tick_lengths.put_nowait(dt)
        except queue.Full:
            fps = self.calculate_fps()
            list(self.entities.values())[0]['Text'].text = fps

    def calculate_fps(self):
        t = 0
        while not self.tick_lengths.empty():
            t += self.tick_lengths.get()
        return self.fps_window / t * 1000

    def render(self, entity):
        text_comp = entity['Text']
        if not text_comp.dirty:
            return

        txt = text_comp.format_str.format(text_comp.text)
        color = text_comp.style.color
        surface = self.font.render(txt, True, color)
        size = self.font.size(txt)
        entity['Visual'].surface = surface
        entity['UITransform'].size = Vector2D(size[0], size[1])
        entity['UITransform'].dirty = True


class Text(entity_component.Component):
    def __init__(self, form='{}', txt=''):
        self.format_str = form
        self.text = txt
        self.dirty = True
        self.style = TextStyle()


class TextStyle(entity_component.Component):
    def __init__(self, color=(0, 0, 0)):
        self.color = color


class Watcher(entity_component.Component):
    def __init__(self, event):
        self.event = event


if __name__ == '__main__':
    pass
