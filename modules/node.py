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
        self.posX = None
        self.posY = None

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