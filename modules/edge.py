from modules.config import *
from modules.node import Node

class Edge(object):
    index = 0
    no_path_tracking_color = DARK_GRAY
    path_tracking_color = LIGHT_BLUE
    path_tracked_color = YELLOW

    def __init__(self):
        self.node_start: Node
        self.node_end: Node
        self.color = Edge.no_path_tracking_color
        self.value = Edge.index
        Edge.index += 1