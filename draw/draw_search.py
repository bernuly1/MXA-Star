import time

import pygame
from map_reader import map_reader
# from corner_search import corner_search
# from corner_search_new import corner_search_new as corner_search
# from a_star import a_star as corner_search
from perfect_runner import p_a_star_runner as corner_search
# from perfect_runner_turbo import p_a_star_turbo as corner_search
# from corner_search_k_new import corner_search_k_new as corner_search
# from sensing_a_star import a_star as corner_search
# from sensing_perfect_runner import sensing_perfect_a_star as corner_search
# from octile.octile_a_star import octile_a_star as corner_search
# from octile.octile_a_star_sensing import octile_a_star_sensing as corner_search
# from octile.perfect_runner_octile import perfect_runner_octile as corner_search
# from octile.perfect_sensing_runner_octile import perfect_sensing_runner_octile as corner_search

# from william.la_a_star import la_a_star as corner_search
from draw.spot import spot
from enums import def_colors as mc
from g_node_3 import g_node

# from corner_search_opt import corner_search_opt as corner_search

clock = pygame.time.Clock()


class draw_search(corner_search):

    def __init__(self, map_reader, map_width, window):
        super().__init__(map_reader)
        self.map_w = map_width
        self.gap1 = 0
        self.gap2 = 0
        self.grid = []
        self.create_grid()
        self.win = window
        # self.start_pos = None
        # self.goal_pos = None
        self.vg_pos = None
        self.vs_pos = None
        self.f_c = 0

    def create_grid(self):
        grid = []
        rows, width = self.map_reader.get_shape()
        self.gap1 = self.map_w // rows
        self.gap2 = self.map_w // width

        for i in range(rows):
            grid.append([])
            for j in range(width):
                _spot = spot(i, j, self.gap1, self.gap2, rows)
                if self.map_reader.is_wall((i, j)):
                    _spot.set_color(mc.wall.value)
                grid[i].append(_spot)
        self.grid = grid

    def add_to_close(self, vn):
        # print(vn.position)
        super().add_to_close(vn)
        if self.map_reader.is_wall(vn.position):
            self.draw_spot(vn.position, mc.wall_closed_list)
        else:
            if vn.f >= 0:
                self.draw_spot(vn.position, mc.closed_list)

            else:
                self.draw_spot(vn.position, mc.path_list)


    def add_to_open(self, vn):
        self.draw_spot(vn.position, mc.open_list)
        super().add_to_open(vn)

            # if vn.position == (259, 188):
        #     self.draw_spot(vn.position, mc.open_list)

    def draw_spot(self, pos, color):
        curr_spot = self.grid[pos[0]][pos[1]]
        rows, width = self.map_reader.get_shape()
        curr_spot.set_color(color.value)
        curr_spot.draw(self.win)
        pygame.display.update()
        # self.draw_grid(rows, width)
        # pygame.display.update()
        # time.sleep(0.13)

    def draw_grid(self, rows, width):
        for i in range(rows):
            pygame.draw.line(self.win, mc.grid_line.value, (0, i * self.gap1), (self.map_w, i * self.gap1))
            for j in range(width):
                pygame.draw.line(self.win, mc.grid_line.value, (j * self.gap2, 0), (j * self.gap2, self.map_w))

    def init_draw(self):
        self.win.fill(mc.non_visited.value)
        rows, width = self.map_reader.get_shape()
        for i in range(rows):
            for j in range(width):
                _spot = self.grid[i][j]
                if (i, j) in [(237, 188), (269, 170)]:  # (259, 186), (278, 186)
                    # if (i, j) in [(259, 231), (260, 231), (260, 232), (261, 232),(261, 233), (262, 234), (265, 235), (266, 237), (268, 238), (269, 240), (271, 241), (272, 244), (348, 243), (349, 240), (351, 238), (352, 235), (354, 234), (355, 232), (352, 231), (350, 229), (347, 228), (345, 226), (342, 225), (341, 223), (338, 222), (336, 220), (333, 219), (331, 216), (328, 215), (327, 213), (324, 212), (323, 210), (320, 209), (318, 207), (318, 205), (317, 203), (315, 202), (314, 199), (316, 197), (315, 196), (313, 195), (312, 197), (309, 198), (307, 196), (305, 195), (303, 195), (300, 194), (298, 192), (296, 191), (294, 189), (291, 188), (290, 186), (288, 185), (287, 188), (285, 189), (283, 189), (280, 188), (278, 186), (275, 185), (274, 183), (271, 182), (269, 180), (266, 179), (265, 176), (267, 174), (268, 171), (270, 170), (271, 166), (273, 165), (274, 163), (272, 162), (273, 159), (273, 159), (271, 157), (269, 156), (267, 154), (266, 156), (264, 156), (261, 155), (259, 153), (248, 152), (247, 155), (245, 156), (240, 158), (240, 157), (241, 154), (244, 153), (245, 150), (247, 149), (245, 148), (245, 146), (246, 143), (246, 143), (244, 141), (242, 140), (241, 138), (238, 137), (237, 135), (234, 134), (233, 132), (231, 131), (229, 129), (227, 128), (58, 128), (56, 129), (55, 131), (53, 133), (52, 135)]:
                    _spot.set_color(mc.path_list.value)
                _spot.draw(self.win)
        # pygame.display.update()
        if self.vg_pos is not None:
            self.set_goal_pos(self.vg_pos)
        if self.vs_pos is not None:
            self.set_start_pos(self.vs_pos)
        # self.draw_grid(rows, width)
        pygame.display.update()

    def add_first_to_close(self, vn):
        super().add_first_to_close(vn)
        if self.map_reader.is_wall(vn.position):
            self.draw_spot(vn.position, mc.wall_closed_list)
        else:
            self.draw_spot(vn.position, mc.closed_list)

    def get_path(self, vn):
        ans = []
        # print("------------------path-------------------")
        current = vn
        self.draw_spot(current.position, mc.goal_position)
        # print(current.position, end =" ")
        current = current.prev
        while current.prev is not None:
            # print(current.position, end =" ")
            self.draw_spot(current.position, mc.path_list)
            current = current.prev
        # print(current.position)
        self.draw_spot(current.position, mc.start_position)
        return super().get_path(vn)

    def search(self):
        # self.vg_pos = vg
        # self.vs_pos = vs
        return super().search(g_node(self.vs_pos), g_node(self.vg_pos))

    def set_start_pos(self, vs):
        if self.vs_pos is None:
            self.vs_pos = vs
        self.draw_spot(self.vs_pos, mc.non_visited)
        self.vs_pos = vs
        self.draw_spot(vs, mc.start_position)

    def set_goal_pos(self, vg):
        if self.vg_pos is None:
            self.vg_pos = vg
        self.draw_spot(self.vg_pos, mc.non_visited)
        self.vg_pos = vg
        self.draw_spot(vg, mc.goal_position)


# MAP_WIDTH = 1782
# MAP_WIDTH = 1562
# MAP_WIDTH = 1100
MAP_WIDTH = 1024
# MAP_WIDTH = 800
# MAP_WIDTH = 682
map_reader = map_reader()


def mousePress(x, das, key):
    t = x[0]
    w = x[1]
    g1 = t // (MAP_WIDTH // das.map_reader.get_shape()[1])
    g2 = w // (MAP_WIDTH // das.map_reader.get_shape()[0])
    print(g2, g1)
    if key == 0:
        das.set_start_pos((g2, g1))
    if key == 1:
        das.set_goal_pos((g2, g1))


def new_draw_instance(start_pos, goal_pos, win, map_reader):
    das = draw_search(map_reader, MAP_WIDTH, win)
    das.init_draw()
    das.set_start_pos(start_pos)
    das.set_goal_pos(goal_pos)
    return das


def start_draw(path, start_pos, goal_pos, map_reader):
    map_reader.create_map(path)
    win = pygame.display.set_mode((MAP_WIDTH, MAP_WIDTH))
    pygame.display.set_caption("corner search")
    das = new_draw_instance(start_pos, goal_pos, win, map_reader)

    while True:
        ev = pygame.event.get()
        for event in ev:
            clock.tick(50)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                mousePress(pos, das, 0)
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                mousePress(pos, das, 1)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("4")
                    start_time = time.time()
                    search_path = das.search()
                    end_time = time.time() - start_time
                    # print(len(search_path))
                    print(
                        f"{end_time}, cost-{search_path[-1].g}, sens-{len(das.sensing)}, gen-{das.count_generated}, exp-{das.count_expanded},"
                        f" switch-{das.lazy_switch}, w-{das.count_wall}, h-{das.start_h}, lgen-{das.local_generated}, lexp-{das.local_expanded}, "
                        f" lw-{das.local_walls}")
                    print("5")
                    # f_c = 0
                    # for key, value in das.hash_open.items():
                    #     if value.f == 231:
                    #         f_c += 1
                    # print(f_c)

                    break
                if event.key == pygame.K_r:
                    das = new_draw_instance(das.vs_pos, das.vg_pos, das.win, das.map_reader)
                    das.create_grid()
                    das.init_draw()
            else:
                continue


#
# 309 152
# 46 55


# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\berlin512.map"
# start_pos = (371, 237)
# goal_pos = (3, 121)
#
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\street\\street-maps\\Berlin_0_512.map"
# start_pos = (371, 237)
# goal_pos = (3, 121)


# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\street\\street-maps\\Berlin_0_256.map"
# start_pos = (72, 248)
# goal_pos = (38, 179)
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\inco_2.map"
# start_pos = (7, 4)
# goal_pos = (8, 21)
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\test_3.map"
# start_pos = (12, 6)
# goal_pos = (22, 22)
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\brc203d_middle.map"
# start_pos = (50, 4)
# goal_pos = (2, 4)
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\random\\random-maps\\random512-40-3.map"


# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\random\\random-maps\\random512-10-1.map"
# start_pos = (414, 125)
# goal_pos = (154, 340)

# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\random\\random-maps\\random-danny.txt"
# start_pos = (339, 58)
# goal_pos = (0, 229)

# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\maze\\maze-maps\\maze512-1-6.map"
# start_pos = (187, 335)
# goal_pos = (185, 359)
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\maze\\maze-maps\\maze512-8-3.map"
# start_pos = (397, 173)
# goal_pos = (303, 199)

# goal_pos = (143, 23)
# (346, 206)
# #
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\dao\\dao-maps\\den510d.map"
# start_pos = (190, 188)
# goal_pos = (218,203)
# (, , , )
# (, , , )
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\street\\street-maps\\Berlin_0_512.map"
# start_pos = (316, 486)
# goal_pos = (292, 295)

# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\random\\random-maps\\random512-20-4.map"
# start_pos  = (100,443)
# goal_pos = (133,436)
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\room\\room-maps\\64room_000.map"
# start_pos = (1,2)
# goal_pos = (3,4)

# start_pos = (314, 446)
# goal_pos = (141, 47)
# start_pos = (233,470)
# goal_pos = (64, 491)
# start_pos = (481, 80)
# goal_pos = (486, 356)
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\brc203d.map"
# start_pos = (45, 35)
# goal_pos = (389, 116)


# start_pos = (229, 41)
# goal_pos = (52, 10)
# start_pos =(48, 72)
# goal_pos = (66, 77)
#
# start_pos = (45, 116)
# goal_pos = (389, 11)
# start_pos = (383, 113)
# goal_pos = (66, 257)
# start_pos = (389, 116)
# goal_pos = (45, 35)
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\presentation.map"
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\test.map"
# start_pos = (14, 7)
# goal_pos = (10, 13)

# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\test_altered.map"
# start_pos = (1, 1)
# goal_pos = (2, 2)
# #
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\test_3_fat.map"
# start_pos = (1, 1)
# goal_pos = (2, 2)
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\inco_4.map"
# start_pos = (1, 1)
# goal_pos = (2, 2)
#

# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\ost003d.map"
# start_pos = (60, 80)
# goal_pos = (184, 112)
# start_pos = (147, 37)
# goal_pos = (83, 166)
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\brc203d.map"
# start_pos = (50, 22)
# goal_pos = (136, 161)
#

# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\bg512\\bg512-maps\\AR0012SR.map"
# start_pos = (379, 358)
# goal_pos = (411, 408)


# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\random\\random-maps\\random512-20-0.map"
# start_pos = (271,190)
# goal_pos = (238, 378)

#

# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\maze\\maze-maps\\maze512-1-7.map"
# start_pos = (311, 252)
# goal_pos = (313, 250)



# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\street\\street-maps\\London_1_512.map"
# start_pos = (508, 19)
# goal_pos = (288, 262)

# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\street\\street-maps\\Denver_0_1024.map"
# start_pos = (49, 5)
# start_pos = (823, 863)
# goal_pos = (907, 954)


# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\random\\random-maps\\random512-15-0.map"
# start_pos = (13,1)
# goal_pos = (212, 323)

# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\street\\street-maps\\Denver_2_256.map"
# start_pos = (162,1)
# goal_pos = (13,255)


# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\random\\random-maps\\random512-40-0.map"
# start_pos = (64, 254)
# goal_pos = (161, 299)
# start_pos = (63, 95)
# goal_pos = (63, 99)

# # #

# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\box_danny_test.map"
# start_pos = (4, 10)
# goal_pos = (12, 9)

# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\half_map.map"
# start_pos = (19, 42)
# goal_pos = (97, 40)

# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\quartor_map.map"
# start_pos = (25, 64)
# goal_pos = (21, 267)
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\isound_big.map"
# start_pos = (513, 987)
# goal_pos = (520, 1074)

# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\plunderisle.map"
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\BOXA\\boxa_algo\\boxa_algo\\maps\\plunderisle_2.map"

# start_pos = (65, 56)
# start_pos = (418, 343)
# goal_pos = (111, 58)
# start_pos = (276, 147)
# goal_pos = (457, 335)
# goal_pos = (100, 25)
# path = "C:\\Users\\User\\OneDrive - post.bgu.ac.il\\Desktop\\maps_moving_ai\\street\\street-maps\\Berlin_0_256.map"
# start_pos = (10, 121)
# goal_pos = (72, 244)


start_draw(path, start_pos, goal_pos, map_reader)
