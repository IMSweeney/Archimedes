from engine.system import System

from engine import logger
_logger = logger.Logger(__name__)

import pygame_gui as pgui
import pygame


class GUIManager(System):
    def __init__(self, window):
        events = [
            'UpdateEvent',
            'WindowResizeEvent',
            'KeyDownEvent',
            'KeyUpEvent',
            'MouseButtonEvent',
            'MouseMotionEvent',
            'UserEvent',
            ''
        ]
        super().__init__(
            set(events),
            set()
        )
        self.window = window
        self.win_size = window.get_size()
        self.manager = pgui.UIManager(self.win_size)

        # self.manager.set_visual_debug_mode(True)

        self.fps = pgui.elements.UILabel(
            relative_rect=pygame.Rect(0, 0, 100, 20),
            text='Hi!',
            manager=self.manager,
            anchors={
                'left': 'left',
                'right': 'left',
                'top': 'top',
                'bottom': 'top',
            })

    def process(self, e):
        if e.type == 'UpdateEvent':
            self.manager.update(e.dt / 1000)
            self.fps.set_text('{}'.format(e.dt))
        elif e.type == 'WindowResizeEvent':
            self.win_size = e.size
        else:
            self.manager.process_events(e.pge)

    def render(self):
        self.manager.draw_ui(self.window)


if __name__ == '__main__':
    pass
