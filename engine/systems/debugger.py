from engine import system
from engine.components.components import *

from engine.uifactory import UIGenerator

from engine import logger
_logger = logger.Logger(__name__)

import pandas as pd


class EntityViewer(system.System):
    def __init__(self, arch_manager):
        super().__init__(
            set(['UpdateEvent']),
            set()
        )
        self.arch_manager = arch_manager
        self.ec_manager = arch_manager.ec_manager
        self.ui_generator = UIGenerator(arch_manager)
        self.timer = Timer(1000)

        self.init_ui()

        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)

    def process(self, e):
        if e.type == 'UpdateEvent':
            if self.timer.update(e.dt):
                self.update_table()

    def update_table(self):
        ent = self.ec_manager.get_entity(self.table_id)
        ent['Text'].text = self.ec_manager.database.head(100)
        ent['Text'].dirty = True

    def init_ui(self):
        base_ui = self.create_base_ui()

        self.table_id = self.create_table(base_ui)
        self.buttons = self.create_buttons(base_ui)

    def create_base_ui(self):
        e = self.ui_generator.generate_empty_ui(
            pos=Vector2D(1, 0),
            size=Vector2D(.3, 1)
        )
        return e

    def create_table(self, parentid):
        e = self.ui_generator.gen_ui_container(
            pos=Vector2D(0, 1),
            size=Vector2D(1, .5),
            parentid=parentid
        )

        components = [
            Text(txt='', wrap=False),
            Scrollable()
        ]

        self.arch_manager.attach_components(e, components)
        return e

    def create_buttons(self, parentid):
        base = self.ui_generator.gen_ui_container(
            pos=Vector2D(0, 0),
            size=Vector2D(1, .5),
            parentid=parentid
        )

        child_ids = []
        for i in range(5):
            e = self.ui_generator.gen_grid_element(parentid=base)
            components = [
                Text(txt='Button {}'.format(i), wrap=False),
                Selectable()
            ]
            self.arch_manager.attach_components(e, components)
            child_ids.append(e)

        self.arch_manager.attach_component(
            base,
            UIGrid(is_vertical=True, child_ids=child_ids)
        )
        return base


class Timer():
    def __init__(self, period):
        self.period = period
        self.t = 0

    def update(self, dt):
        self.t += dt
        if self.t > self.period:
            self.t %= self.period
            return True
        return False


if __name__ == '__main__':
    pass
