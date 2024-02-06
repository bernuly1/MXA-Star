import math

from g_node_3 import g_node
from octile.perfect_runner_octile import perfect_runner_octile


class perfect_sensing_runner_octile(perfect_runner_octile):


    def __init__(self, map_reader):
        super().__init__(map_reader)
        self.sensing = set()


    def get_neighbors(self, vn):
        neighbors_arr = []
        diag_neighbors, direct_neighbors = self.map_reader.get_all_eight_neighbors(vn.position)
        for vertex, is_wall in direct_neighbors:
            successor = g_node(position=vertex,
                               prev=vn)
            successor.g = vn.g + 1
            successor.md = self.base_h_func_min_max(vertex, self.vg.position)
            neighbors_arr.append((successor, 1))
            # yield successor, 1

        for vertex, is_wall in diag_neighbors:
            successor = g_node(position=vertex,
                               prev=vn)
            successor.g = vn.g + 1.5
            successor.md = self.base_h_func_min_max(vertex, self.vg.position)
            if self.is_valid_state(successor):
                neighbors_arr.append((successor, 1.5))
        return neighbors_arr

    def search(self, vs, vg, start_g=0):
        self.start_h = self.base_h_func(vs, vg)
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
            while self.is_wall(current):
                self.add_to_close(current)
                self.count_wall += 1
                self.sensing.add(current.position)
                self.wall_list.add(current.position)
                current = self.get_best()



            if current is None:
                return False
            self.add_to_close(current)
            if self.goal_test(current.position, vg):
                return self.get_path(current)
            else:
                self.count_expanded += 1
                self.sensing.add(current.position)
                for vn, cost in self.get_neighbors(current):
                    # vn.g = current.g + 1
                    # if self.is_wall(vn) == 1:
                    #     if self.is_closed(vn):
                    #         continue


                    # if not self.is_valid_state(vn):
                    #     continue

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

                    elif check_closed and vn.position not in self.wall_list and self.hash_closed[vn.position].g > current.g + cost and self.hash_closed[vn.position].h != math.inf:
                        print("nononononononononononononooooooo")
                        raise Exception("reopen")

        return False


    def get_diag_neighboring_nodes(self, vn):
        pos1 = (vn.prev.position[0], vn.position[1])
        pos2 = (vn.position[0], vn.prev.position[1])
        # if pos1 in self.hash_open:
        #     vn1 = self.hash_open[pos1]
        # else:
        #     vn1 = self.hash_closed[pos1]
        #
        # if pos2 in self.hash_open:
        #     vn2 = self.hash_open[pos2]
        # else:
        #     vn2 = self.hash_closed[pos2]

        return g_node(pos1), g_node(pos2)


    def is_valid_state(self, vn):
        # if self.is_diag_node(vn):
        # vn1, vn2 = self.get_diag_neighboring_nodes(vn)
        # if vn1.position in self.wall_list or vn2.position in self.wall_list:
        #     return False
        # if vn1.position in self.sensing and vn2.position in self.sensing:
        #     return True
        #
        # self.sensing.add(vn1.position)
        #
        # if self.is_wall(vn1):
        #     self.wall_list.add(vn1.position)
        #     self.add_to_close(vn1)
        #     return False
        # else:
        #     self.sensing.add(vn2.position)
        #     if self.is_wall(vn2):
        #         self.add_to_close(vn2)
        #         self.wall_list.add(vn2.position)
        #         return False
        return True
    # return True


    def is_wall(self, vn):
        return self.map_reader.is_wall(vn.position)

    # def search(self, vs, vg, start_g=0):
    #     self.start_h = self.base_h_func(vs, vg)
    #     self.start_g = start_g
    #     self.init_stats()
    #     self.init_open()
    #     self.vg = vg
    #     vs.h = self.base_h_func(vs, vg)
    #     if vs.g is None:
    #         vs.g = 0
    #     self.add_to_open(vs)
    #
    #     while self.open_size() > 0:
    #         current = self.get_best()
    #         while self.is_wall(current):
    #             self.add_to_close(current)
    #             self.count_wall += 1
    #             self.wall_list.add(current.position)
    #             current = self.get_best()
    #
    #
    #         if current is None:
    #             return False
    #         self.add_to_close(current)
    #         if self.goal_test(current.position, vg):
    #             return self.get_path(current)
    #
    #         else:
    #             self.count_expanded += 1
    #             for (vn, cost) in self.get_neighbors(current):
    #                 vn.g = current.g + cost
    #                 # if self.is_wall(vn) == 1:
    #                 #     if self.is_closed(vn):
    #                 #         continue
    #
    #                 # else:
    #                 check_open = self.is_open(vn)
    #                 check_closed = self.is_closed(vn)
    #                 if not check_open and not self.is_closed(vn):
    #                     self.count_generated += 1
    #                     vn.h = self.calc_h(vn, vg)
    #                     vn.prev = current
    #                     self.add_to_open(vn)
    #
    #                 elif check_open and self.hash_open[vn.position].g > current.g + cost:
    #                     vn.h = self.calc_h(vn, vg)
    #                     vn.prev = current
    #                     self.add_to_open(vn)
    #
    #                 elif check_closed and self.hash_closed[vn.position].g > current.g + cost and self.hash_closed[vn.position].h != math.inf:
    #                     print("nononononononononononononooooooo")
    #                     raise Exception("reopen")
    #
    #     return False

    # def get_best(self):
        # while True:
        #     vn = self.get_best_lazy()
        #     if self.is_valid_state(vn):
        #         return vn





    # def get_best_lazy(self):
    #     vn = self.open_list.remove()
    #     while vn.position not in self.hash_open or vn.g > self.hash_open[vn.position].g:
    #         if self.open_size() == 0:
    #             return None
    #         if vn.position in self.hash_open and vn.g == self.hash_open[vn.position].g:
    #             del self.hash_open[vn.position]
    #         vn = self.open_list.remove()
    #     if vn.position in self.hash_open and vn.g == self.hash_open[vn.position].g:
    #         del self.hash_open[vn.position]
    #
    #     done = (vn.generation_iteration == self.last_iteration)
    #     while not done:
    #         curr_h = vn.h
    #         new_h = self.calc_h(vn, self.vg)
    #
    #         if new_h == math.inf:
    #             vn.h = new_h
    #             vn.f = vn.g + vn.h
    #             super().add_to_close(vn)
    #             self.last_iteration += 1
    #             vn = self.open_list.remove()
    #             while vn.position not in self.hash_open or vn.g > self.hash_open[vn.position].g:
    #                 if self.open_size() == 0:
    #                     return None
    #                 if vn.position in self.hash_open and vn.g == self.hash_open[vn.position].g:
    #                     del self.hash_open[vn.position]
    #                 vn = self.open_list.remove()
    #             if vn.position in self.hash_open and vn.g == self.hash_open[vn.position].g:
    #                 del self.hash_open[vn.position]
    #             self.lazy_switch += 1
    #             done = (vn.generation_iteration == self.last_iteration)
    #
    #
    #         elif curr_h < new_h:
    #             vn.h = new_h
    #             vn.f = vn.g + vn.h
    #             self.add_to_open(vn)
    #             vn = self.open_list.remove()
    #             while vn.position not in self.hash_open or vn.g > self.hash_open[vn.position].g:
    #                 if self.open_size() == 0:
    #                     return None
    #                 if vn.position in self.hash_open and vn.g == self.hash_open[vn.position].g:
    #                     del self.hash_open[vn.position]
    #                 vn = self.open_list.remove()
    #             if vn.position in self.hash_open and vn.g == self.hash_open[vn.position].g:
    #                 del self.hash_open[vn.position]
    #             self.lazy_switch += 1
    #             done = (vn.generation_iteration == self.last_iteration)
    #
    #         else:
    #             done = True
    #
    #     return vn