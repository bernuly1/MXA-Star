from g_node_3 import g_node
from perfect_a_start import perfect_a_star


class perfect_a_star_octile(perfect_a_star):


    def __init__(self, map_reader, shape, open_map_reader=None, obstacle_list=None):
        super().__init__(map_reader, shape, open_map_reader)
        self.obstacle_list = obstacle_list

    def get_neighbors(self, vn):
        neighbor_arr = super().get_neighbors(vn)

        x, y = vn.position
        if x > 0 and y > 0:# and not self.is_diag_blocked(vn.position, (-1, -1)):
            pos = (x - 1, y - 1)
            pos = g_node(pos)
            pos.md = self.base_h_func_min_max(pos.position, self.vg.position)
            neighbor_arr.append((pos, 1.5))

        if x < self.shape[0] - 1 and y < self.shape[1] - 1:# and not self.is_diag_blocked(vn.position, (1, 1)):
            pos = (x + 1, y + 1)
            pos = g_node(pos)
            pos.md = self.base_h_func_min_max(pos.position, self.vg.position)
            neighbor_arr.append((pos, 1.5))

        if x < self.shape[0] - 1 and y > 0:# and not self.is_diag_blocked(vn.position, (1, -1)):
            pos = (x + 1, y - 1)
            pos = g_node(pos)
            pos.md = self.base_h_func_min_max(pos.position, self.vg.position)
            neighbor_arr.append((pos, 1.5))

        if x > 0 and y < self.shape[1] - 1:# and not self.is_diag_blocked(vn.position,(-1, 1)):
            pos = (x - 1, y + 1)
            pos = g_node(pos)
            pos.md = self.base_h_func_min_max(pos.position, self.vg.position)
            neighbor_arr.append((pos, 1.5))

        return neighbor_arr

    # def is_diag_blocked(self, position, diag_pos):
    #     x, y = position
    #     n1 = (x+diag_pos[0], y)
    #     n2 = (x, y + diag_pos[1])
    #
    #     n1_cond = (n1 in self.open_map_reader or n1 in self.map_reader) and self.real_map_reader.is_wall(n1) == 1
    #     n2_cond = (n2 in self.open_map_reader or n2 in self.map_reader) and self.real_map_reader.is_wall(n2) == 1
    #
    #     return n1_cond or n2_cond


    def base_h_func(self, v1, v2):
        v1_pos, v2_pos = v1.position, v2.position
        row_distance = abs(v1_pos[1] - v2_pos[1])
        col_distance = abs(v1_pos[0] - v2_pos[0])
        diag_value = 1.5 * min(row_distance, col_distance)
        return diag_value + abs(row_distance - col_distance)


    def is_valid_state(self, vn):
        return True
        # if self.is_diag_node(vn):
        #     vn1, vn2 = self.get_diag_neighboring_nodes(vn)
        #     return not (vn1.position in self.obstacle_list or vn2.position in self.obstacle_list)
        #
        # else:
        #     return True

    def is_diag_node(self, vn):
        return (vn.position[0] - vn.prev.position[0] != 0) and (vn.position[1] - vn.prev.position[1] != 0)

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

    def is_wall(self, vn):
        if vn.position in self.obstacle_list:
            return True
        return super().is_wall(vn)




