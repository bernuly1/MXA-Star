import math

from a_star import a_star
from g_node_3 import g_node

class perfect_a_star(a_star):

    def __init__(self, map_reader, shape, open_map_reader=None):
        super(perfect_a_star, self).__init__(map_reader)
        self.shape = shape
        self.open_map_reader = open_map_reader

    def search(self, vs, vg, start_g=0, min_f=math.inf):
        self.init_open()
        self.init_stats()
        self._vs = vs
        vs = g_node(vs.position)
        vg = g_node(vg.position)
        self.vg = vg
        self.start_g = start_g
        if vs.g is None:
            vs.g = 0
        vs.h = self.base_h_func(vs, vg)
        self.add_to_open(vs)

        while self.open_size() > 0:
            current = self.get_best()
            if current is None:
                return math.inf
            self.add_to_close(current)

            if self.goal_test(current.position, vg):
                return self.get_path(current)

            elif min_f != math.inf and current.f + self.start_g > min_f:
                return self.get_path(current) * -1

            else:
                self.count_expanded += 1
                for (vn, cost) in self.get_neighbors(current):
                    vn.g = current.g + cost
                    vn.prev = current

                    if self.is_wall(vn) == 1:
                        self.count_wall += 1
                        # self.add_to_close(vn)
                        continue

                    elif not self.is_valid_state(vn):
                        continue

                    elif not self.is_open(vn) and not self.is_closed(vn):
                        self.count_generated += 1
                        vn.h = self.base_h_func(vn, vg)
                        self.add_to_open(vn)

                    elif self.is_open(vn) and self.hash_open[vn.position].g > current.g + cost:
                        vn.h = self.base_h_func(vn, vg)
                        self.add_to_open(vn)

                    elif self.is_closed(vn) and self.hash_closed[vn.position].g > current.g + cost:
                        print("nononononononononononononooooooo")
                        raise Exception("reopen")
        return math.inf

    def get_neighbors(self, vn):
        x, y = vn.position
        neighbor_arr = []
        if x > 0:
            pos = (x - 1, y)
            pos = g_node(pos)
            pos.md = self.base_h_func_min_max(pos.position, self.vg.position)
            neighbor_arr.append((pos, 1))
        # below
        if x < self.shape[0] - 1:
            pos = (x + 1, y)
            pos = g_node(pos)
            pos.md = self.base_h_func_min_max(pos.position, self.vg.position)
            neighbor_arr.append((pos, 1))
        # left
        if y > 0:
            pos = (x, y - 1)
            pos = g_node(pos)
            pos.md = self.base_h_func_min_max(pos.position, self.vg.position)
            neighbor_arr.append((pos, 1))
            # right
        if y < self.shape[1] - 1:
            pos = (x, y + 1)
            pos = g_node(pos)
            pos.md = self.base_h_func_min_max(pos.position, self.vg.position)
            neighbor_arr.append((pos, 1))

        return neighbor_arr

    def is_wall(self, vn):
        return vn.position in self.map_reader or\
               (self.open_map_reader is not None and vn.position in self.open_map_reader
                and self.open_map_reader[vn.position] is not None
                and vn.g + self.start_g >= self.open_map_reader[vn.position].g)

    def get_best(self):
        vn = self.open_list.remove()
        while vn.position not in self.hash_open or vn.g > self.hash_open[vn.position].g:
            if self.open_size() == 0:
                return None
            if vn.position in self.hash_open and vn.g == self.hash_open[vn.position].g:
                del self.hash_open[vn.position]
            vn = self.open_list.remove()
        if vn.position in self.hash_open and vn.g == self.hash_open[vn.position].g:
            del self.hash_open[vn.position]

        return vn

    def get_path(self, vn):
        return vn.f
