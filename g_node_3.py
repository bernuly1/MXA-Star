
class g_node:

    def __init__(self, position, prev=None, generation_iteration=0):
        self.position = position
        self.prev = prev
        self.f = None
        self.g = None
        self.h = None
        self.md = None
        self.visible = None
        self.expand_direction = None
        self.generation_iteration = None


    def __lt__(self, other):
        return self.f < other.f or (self.f == other.f and self.h < other.h) or \
           (self.f == other.f and self.h == other.h and self.md[2] < other.md[2]) or \
            (self.f == other.f and self.h == other.h and self.md[2] == other.md[2] and self.position[0] < other.position[0]) or \
               (self.f == other.f and self.h == other.h and self.md[2] == other.md[2] and
                self.position[0] == other.position[0] and self.position[1] <= other.position[1])




    # def __lt__(self, other):
    #     ans =  self.f < other.f or (self.f == other.f and self.h < other.h) or \
    #        (self.f == other.f and self.h == other.h and self.md[0] == other.md[0] and self.generation_iteration > other.generation_iteration)#and self.md[2] < other.md[2]) #or\
               # (self.f == other.f and self.h == other.h and self.md[0] == other.md[0] and self.md[2] == other.md[2]
               #  and self.generation_iteration > other.generation_iteration)
        # return ans





        #or \
           # (self.f == other.f and self.h == other.h and self.md[0] < other.md[0]) or \
                # (self.f == other.f and self.h == other.h and self.md[0] == other.md[0] and self.md[2] == other.md[2] and self.check_straight_line())
            # (self.f == other.f and self.h == other.h and self.md[2] < other.md[2]) #or \
        # (self.f == other.f and self.h == other.h and rand > 0.5)
        # (self.f == other.f and self.h == other.h and self.md[0] == other.md[0] and self.md[1] < other.md[1])


    # def check_straight_line(self):
    #     if self.prev is None or self.prev.prev is None:
    #         return False
    #     return not self.position[0] == self.prev.position[0] == self.prev.prev.position[0] or self.position[1] == self.prev.position[1] == self.prev.prev.position[1]
