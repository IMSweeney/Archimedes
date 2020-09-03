import math


class Component():
    def __init__(self):
        raise NotImplementedError()

    def __repr__(self):
        return str(vars(self))
        # return self.__class__.__name__


class Vector2D(Component):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self, asint=False):
        if not asint:
            return (self.x, self.y)
        else:
            return (int(self.x), int(self.y))

    def to_polar(self):
        mag = (self.x ** 2 + self.y ** 2) ** (1 / 2)
        ang = math.degrees(math.atan2(self.y, self.x))
        return (mag, ang)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        else:
            return Vector2D(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __gt__(self, other):
        return self.x > other.x or self.y > other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '({:.2f}, {:.2f})'.format(self.x, self.y)


class Position(Component):
    def __init__(self, x, y):
        self.position = Vector2D(x, y)


class Visual(Component):
    def __init__(self, surface):
        self.surface = surface


class Animatable(Component):
    def __init__(self, states):
        self.states = []
        self.state_component = None
        self.state_changed = False


class Text(Component):
    def __init__(self, form='{}', txt='', color=(0, 0, 0), wrap=True):
        self.format_str = form
        self.text = txt
        self.dirty = True
        self.wrap = wrap
        self.style = TextStyle(color)


class TextStyle(Component):
    def __init__(self, color=(0, 0, 0)):
        self.color = color


class Watcher(Component):
    def __init__(self, comp, cfield, event, efield):
        self.comp = comp
        self.comp_field = cfield
        self.event = event
        self.event_field = efield


class Linker(Component):
    def __init__(self, comp, entityid, delay=None):
        self.comp = comp
        self.watched_entity = entityid
        self.delay = delay


class Clickable(Component):
    def __init__(self):
        pass


class Selectable(Clickable):
    def __init__(self):
        self.state = False
        self.highlight = True


class Camera(Component):
    def __init__(self):
        pass


class Physics(Component):
    def __init__(self, damping=10):
        self.damping = damping
        self.velocity = Vector2D(0, 0)
        self.applied_forces = Vector2D(0, 0)


class CollisionBox(Component):
    def __init__(self, size=1):
        self.ll_bound = Vector2D(-size / 2, -size / 2)
        self.ur_bound = Vector2D(size / 2, size / 2)
        self.center = Vector2D(0, 0)

    def __repr__(self):
        return '{}, {}'.format(self.ll_bound, self.ur_bound)


class Controlable(Component):
    def __init__(self, force=80):
        self.force = force


class UITransform(Component):
    def __init__(self, x=0, y=0, size=(0, 0), parentid=None, layer=0):
        self.position = Vector2D(x, y)
        self.size = Vector2D(size[0], size[1])
        self.dirty = True
        self.parentid = parentid
        self.layer = layer


class UIConstraints(Component):
    def __init__(self,
                 relative_pos=Vector2D(0, 0),
                 relative_size=None,
                 minimum_size=Vector2D(0, 0),
                 buffer_px=4):
        if not isinstance(relative_pos, Vector2D):
            raise TypeError('relative_pos must be Vector2D')
        if not isinstance(minimum_size, Vector2D):
            raise TypeError('minimum_size must be Vector2D')
        self.relative_pos = relative_pos
        self.relative_size = relative_size
        self.minimum_size = minimum_size
        self.buffer_px = Vector2D(buffer_px, buffer_px)


class UIGrid(Component):
    def __init__(self, child_ids=[],
                 is_vertical=True, is_evenly_spaced=True,
                 px_buffer=0):
        self.is_vertical = is_vertical
        self.is_evenly_spaced = is_evenly_spaced
        self.px_buffer = px_buffer
        self.children = child_ids


class Hoverable(Component):
    def __init__(self, on_delay=0.5, off_delay=0.5):
        self.state = False
        self.is_hovered = False
        self.timer = 0
        self.on_delay = on_delay
        self.off_delay = off_delay


class Scrollable(Component):
    def __init__(self):
        self.dragable = False
        self.position = Vector2D(0, 0)
        self.surface = None
        self.size = Vector2D(0, 0)


class FPSDisplay(Component):
    def __init__(self):
        pass


class Tether(Component):
    def __init__(self, head, tail, max_length=None, surface=None):
        self.max_length = max_length
        self.head = head
        self.tail = tail
        self.surface = surface


if __name__ == '__main__':
    pass
