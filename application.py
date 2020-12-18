from engine import arch_manager
from engine.systems.input_handler import InputHandler
from engine.systems.root_renderer import RootRenderer
from engine.systems.camera import CameraManager
from engine.systems.player_control import PlayerControler
from engine.systems.physics import PhysicsHandler
# from engine.systems.ui_interaction import UIInteraction
# from engine.systems.text_renderer import TextRenderer
# from engine.systems.FPS_system import FPSSystem
# from engine.systems.debugger import EntityViewer
from engine.systems.tether_system import TetherSystem

from engine.gui import UIManager

from engine import tilefactory
from engine import uifactory


class Game():
    def __init__(self):
        self.arch_manager = arch_manager.ArchManager()
        event_manager = self.arch_manager.event_manager
        # ec_manager = self.arch_manager.ec_manager

        TILESIZE = 32

        self.arch_manager.add_systems([
            InputHandler(event_manager),  # should always be first
            RootRenderer(self.arch_manager),
            CameraManager(event_manager),
            PlayerControler(),
            PhysicsHandler(),
            UIManager(),
            # UIInteraction(ec_manager),
            # TextRenderer(ec_manager),
            # FPSSystem(),
            # EntityViewer(self.arch_manager),
            # TetherSystem(self.arch_manager, TILESIZE),
        ])
        world_generator = tilefactory.WorldGenerator(
            self.arch_manager,
            tile_size=TILESIZE
        )
        world_generator.generate_random_map(40)
        p = world_generator.generate_player()
        world_generator.generate_tether(p)

        ui_generator = uifactory.UIGenerator(self.arch_manager)
        ui_generator.generate_ui_elements()

    def run(self):
        self.arch_manager.start(max_framerate=120)


if __name__ == '__main__':
    game = Game()
    game.run()
