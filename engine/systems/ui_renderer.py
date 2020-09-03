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
        entity = {
            comp.__class__.__name__: comp for comp in components
        }
        if entityid in self.entities:
            self.entities.update_data(entityid, entity)
        else:
            parentid = entity['UITransform'].parentid
            self.entities.add_element(
                entityid, entity, parentid=parentid)

    def remove_entity(self, entityid):
        self.entities.remove_element(entityid)

    def process(self, e):
        if e.type == 'WindowResizeEvent':
            self.win_size = Vector2D(e.size[0], e.size[1])
            for node in self.entities:
                entity = self.ec_manager.get_entity(node.guid)
                entity['UITransform'].dirty = True

    def render(self):
        for node in self.entities.breadth_first():
            entity = node.data
            parent = self.get_parent(node)
            self.process_entity(entity, parent, node=node)
            self.render_entity(entity)
            self.render_highlight(entity)

    def process_entity(self, entity, parent, node=None):
        if entity['UITransform'].dirty:
            if 'UIConstraints' in entity:
                self.contraint_manager.process_entity(entity, parent)
            if 'UIGrid' in entity:
                self.grid_manager.process_entity(entity)

            self.calculate_clip(entity, parent)
            # entity['UITransform'].dirty = False

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

    def render_highlight(self, entity):
        if 'Selectable' not in entity:
            return
        elif not entity['Selectable'].highlight:
            return
        elif not entity['Selectable'].state:
            return
        transform = entity['UITransform']
        surface = pygame.Surface(transform.size.to_tuple(), pygame.SRCALPHA)
        pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), width=2)
        self.window.blit(surface, transform.position.to_tuple())

    def get_parent(self, node):
        if node.parent.is_root():
            parent_entity = {
                'UITransform': UITransform(size=self.window.get_size())
            }
        else:
            parent_entity = node.parent.data
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
        if len(grid.children) == 0:
            return

        if grid.is_vertical:
            if grid.is_evenly_spaced:
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
                offset = 0
                total_size = Vector2D(0, 0)
                for i, child_id in enumerate(grid.children):
                    child = self.parent.ec_manager.get_entity(child_id)
                    child['UITransform'].position = Vector2D(
                        transform.position.x,
                        transform.position.y + offset)
                    offset += child['UITransform'].size.y + grid.px_buffer
                    total_size.y = offset
                    total_size.x = max(
                        total_size.x, child['UITransform'].size.x)
        else:
            if grid.is_evenly_spaced:
                child_size = Vector2D(
                    transform.size.x / len(grid.children),
                    transform.size.y)
                for i, child_id in enumerate(grid.children):
                    child = self.parent.ec_manager.get_entity(child_id)
                    child['UITransform'].size = child_size
                    child['UITransform'].position = Vector2D(
                        transform.position.x + child_size.x * i,
                        transform.position.y)
            else:
                offset = 0
                total_size = Vector2D(0, 0)
                for i, child_id in enumerate(grid.children):
                    child = self.parent.ec_manager.get_entity(child_id)
                    child['UITransform'].position = Vector2D(
                        transform.position.x + offset,
                        transform.position.y)
                    offset += child['UITransform'].size.x + grid.px_buffer
                    total_size.y = max(
                        total_size.y, child['UITransform'].size.y)
                    total_size.x = offset

        if 'UIConstraints' not in entity and not grid.is_evenly_spaced:
            transform.size = total_size


class InvalidResizeError(ValueError):
    pass


if __name__ == '__main__':
    pass
