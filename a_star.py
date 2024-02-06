import math

from g_node_3 import g_node
from my_heap import MinHeap

sensing = False
class a_star:

    def __init__(self, map_reader):
        self.map_reader = map_reader
        self.hash_closed = {}
        self.hash_open = {}
        self.open_list = None
        self.vg = None
        self.local_generated = 0
        self.local_expanded = 0
        self.local_walls = 0
        self.sensing = set()
        self.wall_list = set()
        self.generated_before = set()

    def init_stats(self):
        self.count_generated = 0
        self.count_expanded = 0
        self.count_wall = 0
        self.lazy_switch = 0

    def search(self, vs, vg, start_g=0):
        self.start_h = self.base_h_func(vs, vg)
        # self.start_h = self.base_h_func_min_max(vs.position, vg.position)
        self.start_g = start_g
        self.init_stats()
        self.init_open()
        self.vg = vg
        vs.h = self.base_h_func(vs, vg)
        if vs.g is None:
            vs.g = 0
        self.add_to_open(vs)

        while self.open_size() > 0:
            current = self.get_best()
            # if sensing:
            #     while self.is_wall(current):
            #         self.add_to_close(current)
            #         self.count_wall += 1
            #         current = self.get_best()

            if current is None:
                return False
            self.add_to_close(current)
            if self.goal_test(current.position, vg):
                return self.get_path(current)

            else:
                self.count_expanded += 1
                for vn, cost in self.get_neighbors(current):
                    # vn.g = current.g + 1
                    if not sensing:
                        if self.is_wall(vn) == 1:
                            if not self.is_closed(vn):
                                self.count_wall += 1
                                self.sensing.add(vn.position)
                                self.wall_list.add(vn.position)
                                self.add_to_close(vn)
                            continue
                        if not self.is_valid_state(vn):
                            continue

                    # else:
                    check_open = self.is_open(vn)
                    check_closed = self.is_closed(vn)
                    if not check_open and not self.is_closed(vn):
                        if vn.position not in self.generated_before:
                            self.count_generated += 1
                        vn.h = self.calc_h(vn, vg)
                        vn.prev = current
                        self.add_to_open(vn)

                    elif check_open and self.hash_open[vn.position].g > current.g + cost:
                        vn.h = self.calc_h(vn, vg)
                        vn.prev = current
                        self.add_to_open(vn)

                    elif check_closed and self.hash_closed[vn.position].g > current.g + cost and self.hash_closed[vn.position].h != math.inf:
                        print("nononononononononononononooooooo")
                        raise Exception("reopen")


        return False


    def calc_h(self, v1, v2):
        return self.base_h_func(v1, v2)

    def base_h_func(self, v1, v2):
        v1_pos, v2_pos = v1.position, v2.position
        return abs(v1_pos[0] - v2_pos[0]) + abs(v1_pos[1] - v2_pos[1])

    def init_open(self):
        self.open_list = MinHeap()

    def open_size(self):
        return len(self.open_list.heap)

    def add_to_open(self, vn):
        vn.f = vn.g + vn.h
        self.hash_open[vn.position] = vn
        self.open_list.insert(vn)

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

    def add_to_close(self, vn):
        self.hash_closed[vn.position] = vn

    def get_path(self, vn):
        ans = []
        current = vn
        while current is not None:
            ans.insert(0, current)
            current = current.prev
        return ans

    def get_neighbors(self, vn):
        neighbors_arr = []
        neighbors = self.map_reader.get_neighbors(vn.position)
        for vertex, is_wall in neighbors:
            successor = g_node(position=vertex,
                               prev=vn)
            successor.md = self.base_h_func_min_max(vertex, self.vg.position)
            successor.g = vn.g + 1
            if is_wall:
                neighbors_arr.insert(0, (successor, 1))
            else:
                neighbors_arr.append((successor, 1))
        return neighbors_arr

    def is_wall(self, vn):
        return self.map_reader.is_wall(vn.position)

    def is_open(self, vn):
        if vn.position not in self.hash_open or self.hash_open[vn.position] is None:
            return False
        else:
            return True

    def is_closed(self, vn):
        if vn.position not in self.hash_closed or self.hash_closed[vn.position] is None:
            return False
        else:
            return True

    def goal_test(self, current, goal):
        return current == goal.position


    def base_h_func_min_max(self, v1_pos, v2_pos):
        x = abs(v1_pos[0] - v2_pos[0])
        y = abs(v1_pos[1] - v2_pos[1])
        return (x + y), min(x, y), max(x, y)

    def is_valid_state(self, vn):
        return True



