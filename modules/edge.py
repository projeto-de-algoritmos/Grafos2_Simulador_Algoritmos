import pygame
from math import cos, sin, atan, sqrt, pi
from modules.config import *
from modules.node import Node

lenght_rate = 4


class Edge(object):
    index = 0
    no_path_tracking_color = DARK_GRAY
    path_tracking_color = LIGHT_BLUE
    path_tracked_color = YELLOW

    def __init__(self):
        self.__node_start: Node = None
        self.__node_end: Node = None
        self.color = Edge.no_path_tracking_color
        self.value = Edge.index
        self.thickness = 5
        self.lenght = 0
        self.lenght_posX = None
        self.lenght_posY = None
        Edge.index += 1

    @property
    def node_start(self):
        return self.__node_start

    @node_start.setter
    def node_start(self, node):
        self.__node_start = node
        if self.__node_start and self.__node_end:
            self.update_lenght()

    @property
    def node_end(self):
        return self.__node_end

    @node_end.setter
    def node_end(self, node):
        self.__node_end = node
        if self.__node_start and self.__node_end:
            self.update_lenght()

    def update_lenght(self):
        self.lenght = int((sqrt(pow(self.__node_end.posX - self.__node_start.posX, 2) +
                                pow(self.__node_end.posY - self.__node_start.posY, 2))) / 4)
        self.lenght_posX = (self.__node_start.posX +
                            self.__node_end.posX) / 2
        self.lenght_posY = (self.__node_start.posY +
                            self.__node_end.posY) / 2

    def draw(self, screen, font):
        self.update_lenght()
        pygame.draw.line(
            screen, self.color, (
                self.__node_start.posX, self.__node_start.posY), (
                    self.node_end.posX, self.node_end.posY), self.thickness)
        # draw lenght
        node_text = font.render(str(self.lenght), True, RED)
        screen.blit(node_text, (self.lenght_posX, self.lenght_posY))


class EdgeDirected(Edge):
    index = 0
    no_path_tracking_color = DARK_GRAY
    path_tracking_color = LIGHT_BLUE
    path_tracked_color = YELLOW

    def __init__(self):
        self.__node_start: Node = None
        self.__node_end: Node = None
        self.color = Edge.no_path_tracking_color
        self.value = Edge.index
        self.thickness = 5
        self.lenght = 0
        self.lenght_posX = None
        self.lenght_posY = None
        # points of edge arrow
        self.px = (0, 0)
        self.py = (0, 0)
        self.p2 = (0, 0)
        self.p3 = (0, 0)
        self.p4 = (0, 0)
        self.p5 = (0, 0)
        self.p6 = (0, 0)
        self.p7 = (0, 0)
        Edge.index += 1

    @property
    def node_start(self):
        return self.__node_start

    @node_start.setter
    def node_start(self, node):
        self.__node_start = node
        if self.__node_start and self.__node_end:
            self.calculate_arrow()

    @property
    def node_end(self):
        return self.__node_end

    @node_end.setter
    def node_end(self, node):
        self.__node_end = node
        if self.__node_start and self.__node_end:
            self.calculate_arrow()

    def update_lenght(self):
        self.lenght = int((sqrt(pow(self.__node_end.posX - self.__node_start.posX, 2) +
                                pow(self.__node_end.posY - self.__node_start.posY, 2))) / 4)
        self.lenght_posX = (self.__node_start.posX +
                            self.__node_end.posX) / 2
        self.lenght_posY = (self.__node_start.posY +
                            self.__node_end.posY) / 2

    def draw(self, screen, font):
        self.update_lenght()
        self.calculate_arrow()
        pygame.draw.polygon(screen, self.color, ((
            self.px, self.py), self.p2, self.p3, self.p4, self.p5, self.p6, self.p7))
        # draw lenght
        node_text = font.render(str(self.lenght), True, RED)
        screen.blit(node_text, (self.lenght_posX, self.lenght_posY))

    def calculate_arrow(self):
        # nodes coordinates
        node_startX = self.__node_start.posX
        node_startY = self.__node_start.posY
        node_endX = self.__node_end.posX
        node_endY = self.__node_end.posY
        # convert to default coordinates

        edgex_start = node_startX
        edgey_start = node_startY - self.thickness/2
        arrowhead_sizex = 20
        arrowhead_sizey = 20
        node_radius_recoil = self.node_end.radius
        lenghtX = abs(node_endX - node_startX) - \
            arrowhead_sizex - node_radius_recoil
        lenghtY = abs(node_endY - node_startY) - \
            arrowhead_sizey - node_radius_recoil
        lenght = sqrt(pow(lenghtX, 2) + pow(lenghtY, 2))
        # arrow default coordinates
        self.px, self.py = edgex_start, edgey_start
        self.p2 = self.px, self.py + self.thickness
        self.p3 = self.px + lenght, self.p2[1]
        self.p4 = self.p3[0], self.p3[1] + (arrowhead_sizey - self.thickness)/2
        # arrowhead ====
        self.p5 = self.p4[0] + arrowhead_sizex, self.py + self.thickness/2
        # ==============
        self.p6 = self.p4[0], self.p4[1] - arrowhead_sizey
        self.p7 = self.p6[0], self.py

        # tan(angle) = coefficient angular
        try:
            coefficient_angular = (node_endY - node_startY) / \
                (node_endX - node_startX)
            angle = atan(coefficient_angular)
            if angle == 0 and node_endX <= node_startX:
                angle = pi
            elif node_endX <= node_startX:
                angle = -pi + angle
        except:
            # error divide by 0
            if node_endY > node_startY:
                angle = 1.570796
            else:
                angle = -1.570796

        # transform to real rotate
        self.rotate_arrow(angle)

    def rotate_point(self, a, x1, y1, xbase, ybase):
        xbase_rel = (cos(a) * xbase - sin(a)*ybase) - xbase
        ybase_rel = (sin(a) * xbase + cos(a)*ybase) - ybase
        x2 = cos(a) * x1 - sin(a)*y1
        y2 = sin(a) * x1 + cos(a)*y1
        return x2 - xbase_rel, y2 - ybase_rel

    def rotate_arrow(self, angle):
        pbase = (self.px, self.py)
        self.p2 = self.rotate_point(
            angle, self.p2[0], self.p2[1], pbase[0], pbase[1])
        self.p3 = self.rotate_point(
            angle, self.p3[0], self.p3[1], pbase[0], pbase[1])
        self.p4 = self.rotate_point(
            angle, self.p4[0], self.p4[1], pbase[0], pbase[1])
        self.p5 = self.rotate_point(
            angle, self.p5[0], self.p5[1], pbase[0], pbase[1])
        self.p6 = self.rotate_point(
            angle, self.p6[0], self.p6[1], pbase[0], pbase[1])
        self.p7 = self.rotate_point(
            angle, self.p7[0], self.p7[1], pbase[0], pbase[1])
