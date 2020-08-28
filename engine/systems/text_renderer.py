from engine import system
from engine.components.components import *

from engine import logger
_logger = logger.Logger(__name__)

import pygame


class TextRenderer(system.System):
    def __init__(self, ec_manager):
        super().__init__(
            set(['UpdateEvent']),
            set([Text, Visual])
        )
        self.ec_manager = ec_manager
        self.font = pygame.font.SysFont('timesnewroman', 14)

    def process(self, e):
        if e.type == 'UpdateEvent':
            for guid, components in self.entities.items():
                self.render(components)

    def render(self, entity):
        text_comp = entity['Text']
        if not text_comp.dirty:
            return

        parent_size = self.get_parent_size(entity)

        text_comp.dirty = False
        color = text_comp.style.color
        txt = text_comp.format_str.format(text_comp.text)

        lines = txt.split('\n')
        surfaces = []
        size = Vector2D(0, 0)
        for line in lines:
            words = line.split(' ')
            truncated_line = ''
            for word in words:
                next_width = self.font.size(truncated_line + word)[0]
                if next_width > parent_size.x:
                    line_surface = self.font.render(line, True, color)
                    line_size = line_surface.get_rect().size
                    surfaces.append(line_surface)
                    size.x = max(size.x, line_size[0])
                    size.y += line_size[1]
                    truncated_line = ''
                else:
                    truncated_line += word

            if truncated_line != '':
                line_surface = self.font.render(line, True, color)
                line_size = line_surface.get_rect().size

                surfaces.append(line_surface)
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

    def get_parent_size(self, entity):
        pid = entity['UIConstraints'].parentid
        if pid:
            return self.ec_manager.get_entity(pid)['UITransform'].size
        else:
            return Vector2D(100, 100)  # Hack for window as parent


if __name__ == '__main__':
    pass
