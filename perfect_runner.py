import math

from a_star import a_star
from g_node_3 import g_node
from perfect_a_start import perfect_a_star

class p_a_star_runner(a_star):

    def __init__(self, map_reader):
        super().__init__(map_reader)
        self.last_iteration = 0
        self.h_updated = {}


    def calc_h(self, v1, v2):

        if len(self.wall_list) == 0:
            return self.base_h_func(v1, v2)

        if v1.position in self.h_updated and self.h_updated[v1.position][0] == len(self.wall_list) and self.h_updated[v1.position][1] > 0 and self.h_updated[v1.position][1] != math.inf:
            return self.h_updated[v1.position][1]

        p_a_star = self.get_perfect_a_star()
        path_len = p_a_star.search(g_node(v1.position), v2, v1.g, self.get_min_f(v1))
        self.local_generated += p_a_star.count_generated
        self.local_expanded += p_a_star.count_expanded
        self.local_walls += p_a_star.count_wall
        # if v1.position in self.h_updated and self.h_updated[v1.position][0] == len(self.wall_list) and \
        # self.h_updated[v1.position][1] > 0 and path_len != self.h_updated[v1.position][1]:
        #     print(v1.position, self.h_updated[v1.position][1], path_len)
        self.h_updated[v1.position] = (len(self.wall_list), path_len)
        if path_len < 0:
            path_len = path_len * -1
        if path_len == math.inf:
            return math.inf
        return path_len

    def get_best(self):
        # vn = super().get_best()
        return self.get_best_lazy()

    def add_to_open(self, vn):
        super().add_to_open(vn)
        # self.last_dots_generated.append(vn)


    def add_to_close(self, vn):
        super().add_to_close(vn)
        self.last_iteration += 1

    def get_best_lazy(self):
        vn = self.open_list.remove()
        while vn.position not in self.hash_open or vn.g > self.hash_open[vn.position].g:
            if self.open_size() == 0:
                return None
            if vn.position in self.hash_open and vn.g == self.hash_open[vn.position].g:
                del self.hash_open[vn.position]
            vn = self.open_list.remove()
        if vn.position in self.hash_open and vn.g == self.hash_open[vn.position].g:
            del self.hash_open[vn.position]

        done = (vn.generation_iteration == self.last_iteration)
        while not done:
            curr_h = vn.h
            new_h = self.calc_h(vn, self.vg)

            if new_h == math.inf:
                vn.h = new_h
                vn.f = math.inf
                self.generated_before.add(vn.position)
                self.hash_open[vn.position] = vn
                # super().add_to_close(vn)
                self.last_iteration += 1
                vn = self.open_list.remove()
                while vn.position not in self.hash_open or vn.g > self.hash_open[vn.position].g:
                    if self.open_size() == 0:
                        return None
                    if vn.position in self.hash_open and vn.g == self.hash_open[vn.position].g:
                        del self.hash_open[vn.position]
                    vn = self.open_list.remove()
                if vn.position in self.hash_open and vn.g == self.hash_open[vn.position].g:
                    del self.hash_open[vn.position]
                self.lazy_switch += 1
   #             done = (vn.generation_iteration == self.last_iteration)


            elif curr_h < new_h:
                vn.h = new_h
                vn.f = vn.g + vn.h
                self.add_to_open(vn)
                vn = self.open_list.remove()
                while vn.position not in self.hash_open or vn.g > self.hash_open[vn.position].g:
                    if self.open_size() == 0:
                        return None
                    if vn.position in self.hash_open and vn.g == self.hash_open[vn.position].g:
                        del self.hash_open[vn.position]
                    vn = self.open_list.remove()
                if vn.position in self.hash_open and vn.g == self.hash_open[vn.position].g:
                    del self.hash_open[vn.position]
                self.lazy_switch += 1
#                done = (vn.generation_iteration == self.last_iteration)

            else:
                done = True

        return vn

    def search(self, vs, vg, start_g=0):
        self.start_h = self.base_h_func(vs, vg)
        vs = g_node(vs.position)
        vg = g_node(vg.position)
        return super().search(vs, vg, start_g)

    def is_wall(self, vn):
        if super().is_wall(vn):
            if vn.position not in self.hash_closed:
                self.add_to_close(vn)
                self.sensing.add(vn.position)
                self.wall_list.add(vn.position)
                self.count_wall += 1
            return True
        return False


    def get_neighbors(self, vn):
        neighbors = self.map_reader.get_neighbors(vn.position)
        neighbors_arr = []
        for vertex, is_wall in neighbors:
            successor = g_node(position=vertex,
                               prev=vn)#, generation_iteration=vn.generation_iteration + 1)
            successor.md = self.base_h_func_min_max(vertex, self.vg.position)
            successor.g = vn.g + 1
            if is_wall:
                neighbors_arr.insert(0, (successor, 1))
            else:
                neighbors_arr.append((successor, 1))
        return neighbors_arr



    def get_perfect_a_star(self):
        # return perfect_a_star(self.wall_list, self.map_reader.get_shape(), None)
        return perfect_a_star(self.hash_closed, self.map_reader.get_shape(), self.hash_open)

    def get_min_f(self, vn):
        if len(self.open_list.heap) == 0:
            return math.inf
            # return self.base_h_func(vn, self.vg)
        if len(self.open_list.heap) > 0:
            return self.open_list.heap[0].f




