from a_star import a_star
from g_node_3 import g_node


class octile_a_star(a_star):

    def __init__(self, map_reader):
        super(octile_a_star, self).__init__(map_reader)

    def get_neighbors(self, vn):
        diag_neighbors, direct_neighbors = self.map_reader.get_all_eight_neighbors(vn.position)
        for vertex, is_wall in direct_neighbors:
            successor = g_node(position=vertex,
                               prev=vn)
            successor.g = vn.g + 1
            successor.md = self.base_h_func_min_max(vertex, self.vg.position)
            yield successor, 1

        for vertex, is_wall in diag_neighbors:

            successor = g_node(position=vertex,
                               prev=vn)
            successor.g = vn.g + 1.5
            successor.md = self.base_h_func_min_max(vertex, self.vg.position)
            yield successor, 1.5

    def base_h_func(self, v1, v2):
        v1_pos, v2_pos = v1.position, v2.position
        row_distance = abs(v1_pos[1] - v2_pos[1])
        col_distance = abs(v1_pos[0] - v2_pos[0])
        diag_value = 1.5 * min(row_distance, col_distance)
        return diag_value + abs(row_distance - col_distance)


    def base_h_func_min_max(self, v1_pos, v2_pos):
        x = abs(v1_pos[0] - v2_pos[0])
        y = abs(v1_pos[1] - v2_pos[1])
        diag_value = 1.5 * min(x, y)
        return diag_value + abs(x - y), min(x, y), max(x, y)

    def is_valid_state(self, vn):
        return True
        # if self.is_diag_node(vn):
        #     vn1, vn2 = self.get_diag_neighboring_nodes(vn)
        #     return not self.is_wall(vn1) and not self.is_wall(vn2)
        #
        # else:
        #     return True

    def is_diag_node(self, vn):
        return vn.position[0] - vn.prev.position[0] != 0 and vn.position[1] - vn.prev.position[1] != 0

    def get_diag_neighboring_nodes(self, vn):
        pos1 = (vn.prev.position[0], vn.position[1])
        pos2 = (vn.position[0], vn.prev.position[1])
        if pos1 in self.hash_open:
            vn1 = self.hash_open[pos1]
        else:
            vn1 = self.hash_closed[pos1]

        if pos2 in self.hash_open:
            vn2 = self.hash_open[pos2]
        else:
            vn2 = self.hash_closed[pos2]

        return vn1, vn2
    #
    #
    #
    #
    #
    #
    #
    #
