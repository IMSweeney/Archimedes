import sys
sys.path.insert(0, r'C:\Users\ISWEENE\Documents\Projects\Archimedes')

from engine.structures import spatial_hash
from engine.entity_component import Vector2D

import unittest


class Mock():
    def __init__(self, loc):
        self.loc = loc


class TestSpatialHashSize2(unittest.TestCase):
    def setUp(self):
        self.hash = spatial_hash.SpatialHash(2)
        self.ms = []

        # Generate 100 objs
        for i in range(10):
            self.ms.append([])
            for j in range(10):
                m = Mock(Vector2D(i, j))
                self.ms[i].append(m)
                self.hash.add_obj(m, m.loc)

    def test_get_objs_from_point(self):
        pt = Vector2D(0, 0)

        objs = self.hash.get_objs_from_point(pt)
        self.assertEqual(4, len(objs))

    def test_get_objs_from_bounds(self):
        ll = Vector2D(-.5, -.5)
        ur = Vector2D(.5, .5)

        objs = self.hash.get_objs_from_bounds(ll, ur)
        self.assertEqual(4, len(objs))

    def test_get_objs_from_bounds2(self):
        ll = Vector2D(1.40, 1.79)
        ur = Vector2D(2.00, 2.39)

        objs = self.hash.get_objs_from_bounds(ll, ur)
        self.assertEqual(16, len(objs))


if __name__ == '__main__':
    unittest.main()
