from engine import arch_manager
from engine.systems.input_handler import InputHandler
from engine.systems.root_renderer import RootRenderer
from engine.systems.camera import CameraManager
from engine.systems.player_control import PlayerControler
from engine.systems.physics import PhysicsHandler
from engine.systems.ui_interaction import UIInteraction
from engine.systems.text_renderer import TextRenderer

from engine import tilefactory
from engine import uifactory


class Game():
    def __init__(self):
        self.arch_manager = arch_manager.ArchManager()
        event_manager = self.arch_manager.event_manager
        # ec_manager = self.arch_manager.ec_manager

        self.arch_manager.add_systems([
            InputHandler(event_manager),
            RootRenderer(event_manager),
            CameraManager(event_manager),
            PlayerControler(),
            PhysicsHandler(),
            UIInteraction(),
            TextRenderer(),
        ])
        world_generator = tilefactory.WorldGenerator(
            self.arch_manager,
            tile_size=32
        )
        world_generator.generate_random_map(40)
        world_generator.generate_player()

        ui_generator = uifactory.UIGenerator(self.arch_manager)
        ui_generator.generate_ui_elements()

    def run(self):
        self.arch_manager.start(max_framerate=120)


if __name__ == '__main__':
    game = Game()
    game.run()
