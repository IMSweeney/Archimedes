from engine.components.components import *

from engine import logger
_logger = logger.Logger(__name__)

import pygame


class UIGenerator():
    def __init__(self, arch_manager):
        self.arch_manager = arch_manager
        self.alpha = 200
        self.bg_color = (50, 230, 210)
        self.border_color = (20, 20, 250)
        self.border_thickness = 4

        self.font = pygame.font.SysFont(None, 14)
        self.font_color = (255, 255, 255)

    def generate_ui_elements(self):
        self.gen_fps_element()
        self.generate_top_element()
        self.gen_entity_table()

    def generate_empty_ui(self, pos=Vector2D(0, 0),
                          size=None, parentid=None):
        base_size = (200, 200)
        bg = pygame.Surface(base_size).convert()
        bg.fill(self.bg_color)
        bg.set_alpha(self.alpha)
        # pygame.draw.rect(bg, self.border_color,
        #                  bg.get_rect(), self.border_thickness)
        components = [
            Visual(bg),
            UITransform(size=base_size),
            UIConstraints(
                parentid=parentid,
                relative_pos=pos,
                relative_size=size
            ),
        ]
        eid = self.arch_manager.create_entity(components)
        return eid

    def gen_entity_table(self):
        e = self.generate_empty_ui(
            pos=Vector2D(1, 0),
            size=Vector2D(.2, 1)
        )

        components = [
            Visual(pygame.Surface((20, 20)).convert()),
            UITransform(),
            UIConstraints(
                parentid=e,
                relative_pos=Vector2D(0, 0)
            ),
            Text(txt=''),
        ]
        self.arch_manager.create_entity(components)

    def generate_top_element(self):
        e = self.generate_empty_ui(
            pos=Vector2D(.5, 0),
            size=Vector2D(.3, .1)
        )

        components = [
            Visual(pygame.Surface((20, 20)).convert()),
            UITransform(),
            UIConstraints(
                parentid=e,
                relative_pos=Vector2D(0, 0)
            ),
            Selectable(),
            Text(txt=(
                'I am a long line of text with line breaks.\n' +
                'And a little extra\n' +
                'a\n' +
                'a\n' +
                'a\n' +
                'end\n')
            ),
            Hoverable()
        ]
        self.arch_manager.create_entity(components)

    def gen_fps_element(self):
        txt = 'FPS: '
        surface = self.font.render(txt, True, self.font_color)
        size = self.font.size(txt)
        components = [
            Visual(surface),
            UITransform(size=size),
            UIConstraints(
                relative_pos=Vector2D(0, 0),
                # relative_size=Vector2D(.2, .2),
            ),
            Text(form='FPS: {:.0f}', txt=0),
            FPSDisplay(),
        ]
        self.arch_manager.create_entity(components)


if __name__ == '__main__':
    pass
