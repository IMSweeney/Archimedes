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
        if entity['Text'].dirty:
            self.generate_text_surface(entity)
            entity['Text'].dirty = False

        # if entity['UITransform'].dirty:
            # self.clip_text_surface(entity)
        self.clip_text_surface(entity)

    def generate_text_surface(self, entity):
        text_comp = entity['Text']
        parent_size = self.get_parent_transform(entity).size

        color = text_comp.style.color

        txt = text_comp.format_str.format(text_comp.text)

        if text_comp.wrap and parent_size.x != 0:
            lines = self.split_text_by_max_width(txt, parent_size.x)
        else:
            lines = txt.split('\n')

        surfaces = []
        size = Vector2D(0, 0)
        for line in lines:
            line_surface = self.font.render(line, True, color)
            line_size = line_surface.get_rect().size
            surfaces.append(line_surface)
            size.x = max(size.x, line_size[0])
            size.y += line_size[1]

        surface = pygame.Surface(size.to_tuple(), pygame.SRCALPHA)
        line_height = size.y / len(lines)
        for i, line in enumerate(surfaces):
            surface.blit(line, (0, i * line_height))

        entity['Text'].surface = surface
        entity['Text'].size = size
        entity['UITransform'].dirty = True

    def split_text_by_max_width(self, text, max_width):
        truncated_lines = []
        lines = text.split('\n')
        for line in lines:
            words = line.split(' ')
            truncated_line = ''
            for word in words:
                next_width = self.font.size(truncated_line + word)[0]
                if next_width > max_width:
                    truncated_lines.append(truncated_line)
                    truncated_line = ''
                else:
                    truncated_line += ' ' + word

            if truncated_line != '':
                truncated_lines.append(truncated_line)
        return truncated_lines

    def clip_text_surface(self, entity):
        text_comp = entity['Text']
        transform = entity['UITransform']
        visual = entity['Visual']
        parent = self.get_parent_transform(entity)
        if parent.size.x == 0 or text_comp.size < parent.size:
            visual.surface = text_comp.surface
            visual.size = text_comp.size
            return

        clip = parent.size - (transform.position - parent.position)
        transform.size = clip

        if 'Scrollable' in entity:
            scroll_pos = entity['Scrollable'].position
        else:
            scroll_pos = Vector2D(0, 0)

        visual.surface = pygame.Surface(clip.to_tuple(), pygame.SRCALPHA)
        visual.surface.blit(
            text_comp.surface, (0, 0),
            (scroll_pos.x, scroll_pos.y, clip.x, clip.y)
        )

    def get_parent_transform(self, entity):
        pid = entity['UIConstraints'].parentid
        if pid:
            return self.ec_manager.get_entity(pid)['UITransform']
        else:
            return UITransform()


if __name__ == '__main__':
    pass
