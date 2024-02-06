import math
from perfect_runner import p_a_star_runner

class sensing_perfect_a_star(p_a_star_runner):


    def __init__(self, map_reader):
        super().__init__(map_reader)

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
                self.wall_list.add(current.position)
                current = self.get_best()


            if current is None:
                return False
            self.add_to_close(current)
            if self.goal_test(current.position, vg):
                return self.get_path(current)

            else:
                self.count_expanded += 1
                for (vn, cost) in self.get_neighbors(current):
                    vn.g = current.g + cost
                    # if self.is_wall(vn) == 1:
                    #     if self.is_closed(vn):
                    #         continue

                    # else:
                    check_open = self.is_open(vn)
                    check_closed = self.is_closed(vn)
                    if not check_open and not self.is_closed(vn):
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

    def is_wall(self, vn):
        return self.map_reader.is_wall(vn.position)


