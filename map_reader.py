import numpy as np

NUM_OF_START_ROWS = 4


class map_reader:

    def __init__(self):
        self.map = []
        self.shape = None

    # self.map = np.array()

    def create_map(self, map_name):
        with open(map_name, "rt") as infile:
            for i in range(NUM_OF_START_ROWS):
                infile.readline()
            self.map = np.array(([list(line.strip()) for line in infile.readlines()]))
            # return np.array([(list(line.strip())) for line in infile.readlines()])

    def get_all_eight_neighbors(self, position):
        diag_neighbors = self.get_all_diag_neighbors(position)
        direct_neighbors = self.get_neighbors(position)
        return diag_neighbors, direct_neighbors

    def get_sensed_eight_neighbors(self, position):
        diag_neighbors = self.get_sensed_diag_neighbors(position)
        direct_neighbors = self.get_neighbors(position)
        return diag_neighbors, direct_neighbors

    def get_sensed_diag_neighbors(self, position):
        neighbor_arr = []
        x = position[0]
        y = position[1]
        #top left
        if x > 0 and y > 0 and not self.is_wall((x,y - 1)) and not self.is_wall((x - 1,y)):
            pos = (x - 1, y - 1)
            neighbor_arr.append((pos, self.is_wall(pos)))

        #top right
        if x > 0 and y < np.shape(self.map)[1] - 1 and not self.is_wall((x,y + 1)) and not self.is_wall((x - 1,y)):
            pos = (x - 1, y + 1)
            neighbor_arr.append((pos, self.is_wall(pos)))

        # bot right
        if x < np.shape(self.map)[0] - 1 and y < np.shape(self.map)[1] - 1 and not self.is_wall((x,y + 1)) and not self.is_wall((x + 1,y)):
            pos = (x + 1, y + 1)
            neighbor_arr.append((pos, self.is_wall(pos)))

        # bot left
        if x < np.shape(self.map)[0] - 1 and y > 0 and not self.is_wall((x,y - 1)) and not self.is_wall((x + 1,y)):
            pos = (x + 1, y - 1)
            neighbor_arr.append((pos, self.is_wall(pos)))
        return neighbor_arr

    def get_all_diag_neighbors(self, position):
        neighbor_arr = []
        x = position[0]
        y = position[1]
        #top left
        if x > 0 and y > 0:
            pos = (x - 1, y - 1)
            neighbor_arr.append((pos, self.is_wall(pos)))

        #top right
        if x > 0 and y < np.shape(self.map)[1] - 1:
            pos = (x - 1, y + 1)
            neighbor_arr.append((pos, self.is_wall(pos)))

        # bot right
        if x < np.shape(self.map)[0] - 1 and y < np.shape(self.map)[1] - 1:
            pos = (x + 1, y + 1)
            neighbor_arr.append((pos, self.is_wall(pos)))

        # bot left
        if x < np.shape(self.map)[0] - 1 and y > 0:
            pos = (x + 1, y - 1)
            neighbor_arr.append((pos, self.is_wall(pos)))
        return neighbor_arr


    def get_neighbors(self, position):
        neighbor_arr = []
        x = position[0]
        y = position[1]
        #original : above, below, left, right
        # above
        if x > 0:
            pos = (x - 1, y)
            neighbor_arr.append((pos, self.is_wall(pos)))
        # below
        if x < np.shape(self.map)[0] - 1:
            pos = (x + 1, y)
            neighbor_arr.append((pos, self.is_wall(pos)))
        # left
        if y > 0:
            pos = (x, y - 1)
            neighbor_arr.append((pos, self.is_wall(pos)))
            # right
        if y < np.shape(self.map)[1] - 1:
            pos = (x, y + 1)
            neighbor_arr.append((pos, self.is_wall(pos)))
        return neighbor_arr

    def is_legal_pos(self, pos):
        return not (pos[0] < 0 or pos[0] > np.shape(self.map)[0] - 1 or pos[1] < 0 or pos[1] > np.shape(self.map)[1] - 1)

    def is_legal_pivot_pos(self, v1_pos, pivot):
        if not self.is_legal_pos(pivot):
            return False
        return True #self.is_wall(v1_pos) == self.is_wall(pivot)

    def is_wall(self, position):
        if self.map[position[0]][position[1]] == '.':
            return 0
        return 1

    def get_shape(self):
        if self.shape is None:
            self.shape = np.shape(self.map)
        return self.shape


'''
path = "C:\\Users\\Danny\\Desktop\\תואר2\\boxa\\boxa_algo\\maps\\arena.map"
print(path)
x = map_reader()
x.create_map(path)
print(x.get_neighbors((48,48)))

# print(x.__getattribute__(0))
'''
