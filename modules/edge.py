import pygame
from math import cos, sin, atan, sqrt, pi
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


class EdgeDirected(Edge):
    def __init__(self):
        self.node_start: Node
        self.node_end: Node
        self.color = Edge.no_path_tracking_color
        self.value = Edge.index
        Edge.index += 1

    def calculate_arrow(self):
        # Draw arrow
        # nodes coordinates
        nodex_start = 200
        nodey_start = 200
        nodex_end = 100
        nodey_end = 100
        # convert to default coordinates
        edge_thickness = 5
        edgex_start = nodex_start
        edgey_start = nodey_start - edge_thickness/2
        arrowhead_sizex = 20
        arrowhead_sizey = 20
        lenghtX = abs(nodex_end - nodex_start) - arrowhead_sizex
        lenghtY = abs(nodey_end - nodey_start) - arrowhead_sizey
        lenght = sqrt(pow(lenghtX, 2) + pow(lenghtY, 2))
        # arrow default coordinates
        px, py = edgex_start, edgey_start
        p2 = px, py + edge_thickness
        p3 = px + lenght, p2[1]
        p4 = p3[0], p3[1] + (arrowhead_sizey - edge_thickness)/2
        # arrowhead ====
        p5 = p4[0] + arrowhead_sizex, py + edge_thickness/2
        # ==============
        p6 = p4[0], p4[1] - arrowhead_sizey
        p7 = p6[0], py

        # tan(angle) = coefficient angular
        try:
            coefficient_angular = (nodey_end - nodey_start) / \
                (nodex_end - nodex_start)
            angle = atan(coefficient_angular)
            if angle == 0 and nodex_end <= nodex_start:
                angle = pi
            if nodex_end <= nodex_start and nodey_end > nodey_start:
                angle = 1.570796 - angle
            elif nodex_end <= nodex_start and nodey_end <= nodey_start:
                angle = -1.570796 - angle
        except:
            # error divide by 0
            if nodey_end > nodey_start:
                angle = 1.570796
            else:
                angle = -1.570796

        # transform to real rotate
        p2, p3, p4, p5, p6, p7 = self.rotate_arrow(
            angle, (px, py), p2, p3, p4, p5, p6, p7)

        pygame.draw.polygon(self.screen, DARK_GRAY, ((
            px, py), p2, p3, p4, p5, p6, p7))

    def rotate_point(self, a, x1, y1, xbase, ybase):
        xbase_rel = (cos(a) * xbase - sin(a)*ybase) - xbase
        ybase_rel = (sin(a) * xbase + cos(a)*ybase) - ybase
        x2 = cos(a) * x1 - sin(a)*y1
        y2 = sin(a) * x1 + cos(a)*y1
        return x2 - xbase_rel, y2 - ybase_rel

    def rotate_arrow(self, angle, pbase, p2, p3, p4, p5, p6, p7):
        p2 = self.rotate_point(angle, p2[0], p2[1], pbase[0], pbase[1])
        p3 = self.rotate_point(angle, p3[0], p3[1], pbase[0], pbase[1])
        p4 = self.rotate_point(angle, p4[0], p4[1], pbase[0], pbase[1])
        p5 = self.rotate_point(angle, p5[0], p5[1], pbase[0], pbase[1])
        p6 = self.rotate_point(angle, p6[0], p6[1], pbase[0], pbase[1])
        p7 = self.rotate_point(angle, p7[0], p7[1], pbase[0], pbase[1])
        return p2, p3, p4, p5, p6, p7
