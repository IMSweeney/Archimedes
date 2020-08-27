from engine import system
from engine.components.components import *

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
        self.font = pygame.font.SysFont('timesnewroman', 14)

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
        # if not text_comp.dirty:
        #     return

        if text_comp.format_str == '{}':
            text_comp.text = '{}\n{}'.format(
                entity['UITransform'].position, entity['UITransform'].size
            )

        # text_comp.dirty = False
        color = text_comp.style.color
        txt = text_comp.format_str.format(text_comp.text)
        lines = txt.split('\n')
        surfaces = []
        size = Vector2D(0, 0)
        for line in lines:
            line_surface = self.font.render(line, True, color)
            surfaces.append(line_surface)
            line_size = self.font.size(line)
            size.x = max(size.x, line_size[0])
            size.y += line_size[1]

        surface = pygame.Surface(size.to_tuple(), pygame.SRCALPHA)
        line_height = size.y / len(lines)
        for i, line in enumerate(surfaces):
            surface.blit(
                line, (0, i * line_height))

        entity['Visual'].surface = surface
        entity['UITransform'].size = size
        entity['UITransform'].dirty = True


if __name__ == '__main__':
    pass
