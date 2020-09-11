from engine import system
from engine.components.components import *

from engine import logger
_logger = logger.Logger(__name__)


class PlayerControler(system.System):
    def __init__(self):
        super().__init__(
            set(['UpdateEvent', 'KeyDownEvent', 'KeyUpEvent']),
            set([Position, Physics, Controlable])
        )
        self.move_keys = {
            100: Vector2D(1, 0),
            97: Vector2D(-1, 0),
            119: Vector2D(0, 1),
            115: Vector2D(0, -1),
        }
        self.place_tether_key = 32  # Space

    def process(self, e):
        if e.type == 'UpdateEvent':
            for guid, components in self.entities.items():
                pass

        elif e.type == 'KeyDownEvent':
            if e.key_code in self.move_keys:
                for guid, components in self.entities.items():
                    components['Physics'].applied_forces[e.key_code] = (
                        self.move_keys[e.key_code] *
                        components['Controlable'].force)
            elif e.key_code == self.place_tether_key:
                self.place_tether_anchor()

        elif e.type == 'KeyUpEvent':
            if e.key_code in self.move_keys:
                for guid, components in self.entities.items():
                    components['Physics'].applied_forces.pop(
                        e.key_code)

    def place_tether_anchor(self):
        for guid, components in self.entities.items():
            _logger.info(components['Position'])


if __name__ == '__main__':
    pass
