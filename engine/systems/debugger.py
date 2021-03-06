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

        self.MAX_ROWS = 30

        self.init_ui()

        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', None)

    def process(self, e):
        if e.type == 'UpdateEvent':
            if self.timer.update(e.dt):
                self.update_table()

    def update_table(self):
        ent = self.ec_manager.get_entity(self.table_id)
        self.update_buttons()
        active_cols = self.get_active_columns()
        df = self.ec_manager.database[active_cols]
        df = df.dropna(how='all')
        ent['Text'].text = df.head(self.MAX_ROWS)
        ent['Text'].dirty = True

    def update_buttons(self):
        df = self.ec_manager.database
        if len(self.buttons) != len(df.columns):
            for button in self.buttons:
                self.arch_manager.remove_entity(button)
            self.buttons = self.create_buttons(
                self.button_section, component_names=df.columns)

    def get_active_columns(self):
        buttons = self.ec_manager.get_entity_components_from_ids(self.buttons)
        active_cols = [
            button['Text'].text for button in buttons
            if button['Selectable'].state
        ]
        return active_cols

    def init_ui(self):
        self.base_ui = self.create_base_ui()

        self.button_section = self.ui_generator.gen_grid_element(
            # size=Vector2D(1, .2),
            parentid=self.base_ui)

        self.table_id = self.create_table(self.base_ui)

        self.arch_manager.attach_components(self.base_ui, [
            UIGrid(
                child_ids=[self.button_section, self.table_id],
                is_vertical=False, is_evenly_spaced=False,
                px_buffer=20),
        ])

        self.buttons = []

    def create_base_ui(self):
        e = self.ui_generator.generate_empty_ui(
            pos=Vector2D(1, 0),
            size=Vector2D(.3, 1)
        )
        return e

    def create_table(self, parentid):
        # e = self.ui_generator.gen_ui_container(
        #     pos=Vector2D(0, .2),
        #     size=Vector2D(1, .8),
        #     parentid=parentid
        # )

        e = self.ui_generator.gen_grid_element(
            parentid=parentid)
        components = [
            Text(txt='', wrap=False),
            Scrollable(),
        ]
        self.arch_manager.attach_components(e, components)
        return e

    def create_buttons(self, parentid, component_names=[]):
        child_ids = []
        for component_name in component_names:
            e = self.ui_generator.gen_grid_element(parentid=parentid)
            components = [
                Text(txt=component_name, wrap=False),
                Selectable()
            ]
            self.arch_manager.attach_components(e, components)
            child_ids.append(e)

        self.arch_manager.attach_components(parentid, [
            UIGrid(
                child_ids=child_ids,
                is_vertical=True,
                is_evenly_spaced=False,
                px_buffer=4),
            Scrollable()
        ])
        return child_ids


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
