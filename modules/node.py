import pygame

from modules.config import *


class Node(object):
    indexes_used = []
    path_tracking_color = LIGHT_BLUE
    path_tracked_color = GREEN
    path_tracked_middle_color = YELLOW

    def __init__(self, value):
        try:
            if value in self.indexes_used:
                raise AttributeError
            self.value = value
            Node.indexes_used.append(value)
        except AttributeError:
            print('value node (%d) already used' % (value))
            exit()
        self.neighbors = []
        self.color = None
        self.__original_color = None
        self.__posX = None
        self.__posY = None
        self.radius = NODE_RADIUS
        self.txt_posX = None
        self.txt_posY = None

    @property
    def posX(self):
        return self.__posX

    @property
    def posY(self):
        return self.__posY

    @posX.setter
    def posX(self, pos):
        self.__posX = pos
        self.txt_posX = self.calc_txt_node(self.posX)

    @posY.setter
    def posY(self, pos):
        self.__posY = pos
        self.txt_posY = self.calc_txt_node(self.posY)

    @property
    def original_color(self):
        return self.__original_color

    @original_color.setter
    def original_color(self, new_color):
        self.__original_color = new_color
        self.color = self.__original_color

    def add_neighbor(self, node, edge):
        neighbor = type('', (), {})()
        neighbor.node = node
        neighbor.edge = edge
        self.neighbors.append(neighbor)

    def get_value_neighbors(self):
        values = []
        for neighbor in self.neighbors:
            values.append(neighbor.value)
        return values

    def calc_txt_node(self, pos):
        return pos - self.radius / \
            (self.radius * 4 / NODE_RADIUS_DEFAULT)
