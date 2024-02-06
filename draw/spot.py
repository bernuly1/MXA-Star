import pygame
from enums import colors as mc


class spot:
    def __init__(self, row, col, width, height, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.total_rows = total_rows
        self.y = row * width
        self.x = col * height
        self.color = mc.WHITE.value

    def get_pos(self):
        return self.row, self.col

    def set_color(self, color):
        self.color = color

    def draw(self, _win):
        pygame.draw.rect(_win, self.color, (self.x, self.y, self.height, self.width))
