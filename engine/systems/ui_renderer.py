from engine import system
from engine.components.components import *
from engine.structures.tree import Tree

from engine import logger
_logger = logger.Logger(__name__)

import pygame


class UIRenderer(system.System):
    def __init__(self, window, ec_manager):
        super().__init__(
            set(['WindowResizeEvent']),
            set([UITransform, Visual])
        )
        self.ec_manager = ec_manager
        self.window = window
        size = window.get_size()
        self.win_size = Vector2D(size[0], size[1])
        self.entities = Tree()

        self.contraint_manager = RelativeConstraintsManager()
        self.grid_manager = GridConstraintManager(self)

    def add_entity(self, entityid, components):
        if entityid in self.entities:
            return
        entity = {
            comp.__class__.__name__: comp for comp in components
        }
        parentid = entity['UITransform'].parentid
        self.entities.add_element(entityid, parentid=parentid)

    def remove_entity(self, entityid):
        self.entities.remove_element(entityid)

    def process(self, e):
        if e.type == 'WindowResizeEvent':
            self.win_size = Vector2D(e.size[0], e.size[1])
            for node in self.entities:
                entity = self.ec_manager.get_entity(node.guid)
                entity['UITransform'].dirty = True

    def render(self):
        for child in self.entities.breadth_first():
            entity = self.ec_manager.get_entity(child.guid)
            self.process_entity(entity)
            self.render_entity(entity)

    def process_entity(self, entity):
        if entity['UITransform'].dirty:
            parent = self.get_parent(entity)
            if 'UIConstraints' in entity:
                self.contraint_manager.process_entity(entity, parent)
            if 'UIGrid' in entity:
                self.grid_manager.process_entity(entity)

            self.calculate_clip(entity, parent)
            entity['UITransform'].dirty = False

    def calculate_clip(self, entity, parent):
        parent_size = parent['UITransform'].size

        if 'Scrollable' in entity:
            scroll_pos = entity['Scrollable'].position
        else:
            scroll_pos = Vector2D(0, 0)
        entity['UITransform'].clip = (
            scroll_pos.x, scroll_pos.y,
            parent_size.x, parent_size.y
        )

    def render_entity(self, entity):
        clip = entity['UITransform'].clip
        child_surface = entity['Visual'].surface
        pos = entity['UITransform'].position
        self.window.blit(child_surface, pos.to_tuple(), clip)

    def get_parent(self, entity):
        pid = entity['UITransform'].parentid
        if pid:
            parent_entity = self.ec_manager.get_entity(pid)
        else:
            parent_entity = {
                'UITransform': UITransform(size=self.window.get_size())
            }
        return parent_entity


class RelativeConstraintsManager():
    def __init__(self):
        pass

    def process_entity(self, entity, parent):
        parent_pos = parent['UITransform'].position
        parent_size = parent['UITransform'].size

        self.scale_element(entity, parent_pos, parent_size)
        self.calculate_transform(entity, parent_pos, parent_size)

    def calculate_transform(self, entity, parent_pos, parent_size):
        constraints = entity['UIConstraints']
        transform = entity['UITransform']

        max_pos = (
            parent_pos + parent_size -
            transform.size -
            (2 * constraints.buffer_px))

        transform.position = (
            parent_pos + constraints.buffer_px +
            constraints.relative_pos * max_pos)

    def scale_element(self, entity, parent_pos, parent_size):
        constraints = entity['UIConstraints']
        transform = entity['UITransform']
        visual = entity['Visual']

        if not constraints.relative_size:
            pass
        else:
            size = constraints.relative_size * parent_size
            if size < constraints.minimum_size:
                raise InvalidResizeError()

            transform.size = size
            visual.surface = pygame.transform.scale(
                visual.surface, size.to_tuple(asint=True)
            )


class GridConstraintManager():
    def __init__(self, parent):
        self.parent = parent

    def process_entity(self, entity):
        grid = entity['UIGrid']
        transform = entity['UITransform']

        if grid.is_vertical:
            child_size = Vector2D(
                transform.size.x,
                transform.size.y / len(grid.children))
            for i, child_id in enumerate(grid.children):
                child = self.parent.ec_manager.get_entity(child_id)
                child['UITransform'].size = child_size
                child['UITransform'].position = Vector2D(
                    transform.position.x,
                    transform.position.y + child_size.y * i)
        else:
            child_size = Vector2D(
                transform.size.x / len(grid.children),
                transform.size.y)
            for i, child_id in enumerate(grid.children):
                child = self.parent.ec_manager.get_entity(child_id)
                child['UITransform'].size = child_size
                child['UITransform'].position = Vector2D(
                    transform.position.x + child_size.x * i,
                    transform.position.y)


class InvalidResizeError(ValueError):
    pass


if __name__ == '__main__':
    pass
