
class Component():
    def __init__(self):
        raise NotImplementedError()


class Vector2D(Component):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self, asint=False):
        if not asint:
            return (self.x, self.y)
        else:
            return (int(self.x), int(self.y))

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
        self.__mul__(other)

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
    def __init__(self, form='{}', txt='', color=(0, 0, 0)):
        self.format_str = form
        self.text = txt
        self.dirty = True
        self.style = TextStyle(color)


class TextStyle(Component):
    def __init__(self, color=(0, 0, 0)):
        self.color = color


class Watcher(Component):
    def __init__(self, event):
        self.event = event


class Clickable(Component):
    def __init__(self):
        pass


class Selectable(Clickable):
    def __init__(self):
        self.state = False


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
    def __init__(self, x=0, y=0, size=(0, 0)):
        self.position = Vector2D(x, y)
        self.size = Vector2D(size[0], size[1])
        self.dirty = True


class UIConstraints(Component):
    def __init__(self, parentid=None,
                 relative_pos=Vector2D(0, 0),
                 relative_size=None,
                 minimum_size=Vector2D(0, 0)):
        self.parentid = parentid
        self.relative_pos = relative_pos
        self.relative_size = relative_size
        self.minimum_size = minimum_size


if __name__ == '__main__':
    pass
