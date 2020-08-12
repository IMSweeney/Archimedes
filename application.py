from engine import arch_manager
from engine.system_input_handler import InputHandler
from engine.system_renderer import Renderer
from engine.system_camera import CameraManager
from engine.system_player_control import PlayerControler
from engine.sys_physics import PhysicsHandler

from engine import tilefactory


class Game():
    def __init__(self):
        self.arch_manager = arch_manager.ArchManager()
        event_manager = self.arch_manager.event_manager
        ec_manager = self.arch_manager.ec_manager
        self.arch_manager.add_systems([
            InputHandler(event_manager),
            Renderer(ec_manager, tile_size=32),
            CameraManager(event_manager, ec_manager),
            PlayerControler(ec_manager),
            PhysicsHandler()
        ])
        world_generator = tilefactory.WorldGenerator(
            self.arch_manager,
            tile_size=32
        )
        world_generator.generate_random_map(20)
        world_generator.generate_player()

    def run(self):
        self.arch_manager.start(max_framerate=120)


if __name__ == '__main__':
    game = Game()
    game.run()
