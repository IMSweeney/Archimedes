import math


class SpatialHash():
    def __init__(self, size):
        self.table = {}
        self.size = size

    def clear(self):
        self.table = {}

    def add_obj(self, obj, location):
        h_key = self.hash_location(location)
        self.add_obj_to_bin(obj, h_key)

    def add_obj_to_bin(self, obj, h_key):
        if h_key not in self.table:
            self.table[h_key] = set()
        self.table[h_key].add(obj)

    # def update_location(self, obj):
    #     h_key_old = self.hash_location(obj.old_tile_location)
    #     h_key_new = self.hash_location(obj.tile_location)
    #     if h_key_old != h_key_new:
    #         self.remove_obj(obj, h_key_old)
    #         self.add_obj_to_bin(obj, h_key_new)

    # def remove_obj(self, obj, h_key):
    #     self.table[h_key].discard(obj)

    def get_objs_from_point(self, point):
        h_key = self.hash_location(point)
        if h_key in self.table:
            return self.table[h_key]
        else:
            return []

    def get_objs_from_bounds(self, ll_bound, ur_bound):
        objs = []
        h1 = self.hash_location(ll_bound)
        h2 = self.hash_location(ur_bound)
        for i in range(h1[0], h2[0] + 1):
            for j in range(h1[1], h2[1] + 1):
                if (i, j) in self.table:
                    objs += self.table[(i, j)]

        return objs

    def get_objs(self):
        objs = set()
        for k, v in self.table.items():
            objs |= v
        return list(objs)

    def hash_location(self, location):
        x = math.floor(location.x / self.size)
        y = math.floor(location.y / self.size)
        return (x, y)

    def __contains__(self, obj):
        h_key = self.hash_location(obj.old_tile_location)
        return h_key in self.table and obj in self.table[h_key]

    def __repr__(self):
        msg = 'Bin size: {}\n'.format(self.size)
        for k, v in self.table.items():
            msg += '{}: {}\n'.format(k, len(v))
        return msg
