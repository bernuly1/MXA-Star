from g_node_3 import g_node
from perfect_a_start import perfect_a_star


class perfect_octile(perfect_a_star):

    def __init__(self, map_reader, shape, open_map_reader=None, wall_list=None):
        super(perfect_octile, self).__init__(map_reader, shape, open_map_reader)

    def get_neighbors(self, vn):
        x, y = vn.position
        neighbor_arr = []
        if x > 0:
            pos = (x - 1, y)
            pos = g_node(pos)
            neighbor_arr.append((pos, 1))
        # below
        if x < self.shape[0] - 1:
            pos = (x + 1, y)
            pos = g_node(pos)
            neighbor_arr.append((pos, 1))
        # left
        if y > 0:
            pos = (x, y - 1)
            pos = g_node(pos)
            neighbor_arr.append((pos, 1))
            # right
        if y < self.shape[1] - 1:
            pos = (x, y + 1)
            pos = g_node(pos)
            neighbor_arr.append((pos, 1))

        #top left
        if x > 0 and y > 0:
            pos = (x - 1, y - 1)
            pos = g_node(pos)
            neighbor_arr.append((pos, 1.5))
        # top right

        if x > 0 and y < self.shape[1] - 1:
            pos = (x - 1, y + 1)
            pos = g_node(pos)
            neighbor_arr.append((pos, 1.5))

        # bot right
        if x < self.shape[0] - 1 and y < self.shape[1] - 1:
            pos = (x + 1, y + 1)
            pos = g_node(pos)
            neighbor_arr.append((pos, 1.5))
        # bot left
        if x < self.shape[0] - 1 and y > 0:
            pos = (x + 1, y - 1)
            pos = g_node(pos)
            neighbor_arr.append((pos, 1.5))


        return neighbor_arr

    def base_h_func_min_max(self, v1_pos, v2_pos):
        x = abs(v1_pos[0] - v2_pos[0])
        y = abs(v1_pos[1] - v2_pos[1])
        diag_value = 1.5 * min(x, y)
        return diag_value + abs(x - y), min(x, y), max(x, y)

    def base_h_func(self, v1, v2):
        v1_pos, v2_pos = v1.position, v2.position
        row_distance = abs(v1_pos[1] - v2_pos[1])
        col_distance = abs(v1_pos[0] - v2_pos[0])
        diag_value = 1.5 * min(row_distance, col_distance)
        return diag_value + abs(row_distance - col_distance)






