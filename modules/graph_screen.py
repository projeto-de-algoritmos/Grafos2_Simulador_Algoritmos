import pygame
import pygame.gfxdraw
from pygame.locals import *
import random
from math import cos, sin
from modules.config import *
from modules.screen_objects import Button


def rotate_point(a, x1, y1, xbase, ybase):
    xbase_rel = (cos(a) * xbase - sin(a)*ybase) - xbase
    ybase_rel = (sin(a) * xbase + cos(a)*ybase) - ybase
    x2 = cos(a) * x1 - sin(a)*y1
    y2 = sin(a) * x1 + cos(a)*y1
    return x2 - xbase_rel, y2 - ybase_rel


def rotate_arrow(angle, pbase, p2, p3, p4, p5, p6, p7):
    p2 = rotate_point(angle, p2[0], p2[1], pbase[0], pbase[1])
    p3 = rotate_point(angle, p3[0], p3[1], pbase[0], pbase[1])
    p4 = rotate_point(angle, p4[0], p4[1], pbase[0], pbase[1])
    p5 = rotate_point(angle, p5[0], p5[1], pbase[0], pbase[1])
    p6 = rotate_point(angle, p6[0], p6[1], pbase[0], pbase[1])
    p7 = rotate_point(angle, p7[0], p7[1], pbase[0], pbase[1])
    return p2, p3, p4, p5, p6, p7


class GraphScreen(object):
    def __init__(self, screen, screen_manager, clock):
        self.screen = screen
        self.screen_manager = screen_manager
        self.clock = clock
        self.font = pygame.font.Font(
            'modules/fonts/roboto/Roboto-Black.ttf', 15)

        # graph
        self.graph = None
        self.nodes = []
        self.edges = []
        self.enqueue_nodes = []
        self.search_algorithm1 = None
        self.search_algorithm2 = None
        self.search_algorithm_current = None
        self.generate_graph = None

        # objects
        self.text_warning = ''
        self.button_menu = Button('Menu', 20, SCREEN_HEIGHT - 50)
        self.button_type_bfs = Button(
            'BFS', SCREEN_WIDTH - 120, SCREEN_HEIGHT - 50)
        self.button_type_dfs = Button(
            'DFS', SCREEN_WIDTH - 60, SCREEN_HEIGHT - 50)
        self.button_current_search = None

    def start(self, qtt_nodes, qtt_edges):
        self.nodes = []
        self.edges = []
        self.button_type_bfs.clicked()
        self.button_current_search = self.button_type_bfs
        self.generate_graph(qtt_nodes, qtt_edges)

    def set_graph(self, graph):
        self.graph = graph

    def set_generate_graph(self, generate_graph):
        self.generate_graph = generate_graph

    def set_search_algorithm(self, search_algorithm1=None, search_algorithm2=None):
        self.search_algorithm1 = search_algorithm1
        self.search_algorithm2 = search_algorithm2
        self.search_algorithm_current = search_algorithm1

    def set_search_algorithm_current(self, search_algorithm):
        self.search_algorithm_current = search_algorithm

    def draw(self, clock_fps=30):
        # redraw screen
        self.screen.fill(LIGHT_GRAY)
        # Draw edges
        for edge in self.edges:
            pygame.draw.line(
                self.screen, edge.color, (edge.node_start.posX,
                                          edge.node_start.posY), (edge.node_end.posX, edge.node_end.posY), 3)
        # Draw Nodes
        for node in self.nodes:
            node_text = self.font.render(str(node.value), True, WHITE)
            pygame.gfxdraw.filled_circle(
                self.screen, node.posX, node.posY, node.radius, node.color)
            self.screen.blit(node_text, (node.txt_posX, node.txt_posY))

        # Draw arrow
        # nodes coordinates
        nodex_start = 200
        nodey_start = 200
        nodex_end = 300
        nodey_end = 200
        # convert to default coordinates
        edge_thickness = 5
        edgex_start = 200
        edgey_start = 200 - edge_thickness/2
        edgex_end = 300
        edgey_end = edgey_start
        arrowhead_sizex = 10
        arrowhead_sizey = 20
        # arrow coordinates
        px, py = edgex_start, edgey_start
        p2 = px, py + edge_thickness
        p3 = edgex_end - arrowhead_sizex, p2[1]
        p4 = p3[0], p3[1] + (arrowhead_sizey - edge_thickness)/2
        # arrowhead ====
        p5 = p4[0] + arrowhead_sizex, py + edge_thickness/2
        # ==============
        p6 = p4[0], p4[1] - arrowhead_sizey
        p7 = p6[0], py

        pygame.draw.polygon(self.screen, BLACK, ((
            px, py), p2, p3, p4, p5, p6, p7))

        p2, p3, p4, p5, p6, p7 = rotate_arrow(
            0.5, (px, py), p2, p3, p4, p5, p6, p7)

        pygame.draw.polygon(self.screen, BLACK, ((
            px, py), p2, p3, p4, p5, p6, p7))

        # Draw Buttons
        self.button_menu.draw(self.screen)
        self.button_type_bfs.draw(self.screen)
        self.button_type_dfs.draw(self.screen)

        # render warning
        label_warning = self.font.render(self.text_warning, True, RED)
        self.screen.blit(label_warning,
                         (SCREEN_WIDTH / 4, SCREEN_HEIGHT - 30))

        pygame.display.flip()
        self.clock.tick(clock_fps)

    def keys_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEMOTION:
                if event.buttons[2]:
                    # clicked on right button and moving
                    position = pygame.mouse.get_pos()
                    rel = event.rel
                    self.change_nodes_pos(rel[0], rel[1])
                if event.buttons[0]:
                    # clicked on left button to drag node
                    position = pygame.mouse.get_pos()
                    node = self.selected_node(position)
                    if node is not None:
                        rel = event.rel
                        self.change_node_pos(node, rel[0], rel[1])

            elif event.type == pygame.MOUSEBUTTONUP:
                # if left button is clicked on node
                position = pygame.mouse.get_pos()
                node = self.selected_node(position)
                if node is not None:
                    self.cache_enqueue_selected_nodes(node)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # if clicked on Button Menu
                if self.button_menu.box.collidepoint(event.pos):
                    self.button_menu.clicked()
                    self.screen_manager.switch_to_menu()

                if self.button_type_bfs.box.collidepoint(event.pos):
                    if self.button_type_bfs.active is False:
                        self.button_type_bfs.clicked()
                        self.button_current_search.clicked()
                        self.button_current_search = self.button_type_bfs

                        # set search algorithm
                        self.set_search_algorithm_current(
                            self.search_algorithm1)

                if self.button_type_dfs.box.collidepoint(event.pos):
                    if self.button_type_dfs.active is False:
                        self.button_type_dfs.clicked()
                        self.button_current_search.clicked()
                        self.button_current_search = self.button_type_dfs

                        # set search algorithm
                        self.set_search_algorithm_current(
                            self.search_algorithm2)

    def create_node(self, node):

        self.nodes.append(node)

        return node

    def add_edge(self, edge):
        # create edge of a node
        self.edges.append(edge)

    def remove_edge(self):
        # remove an edge
        self.edges.pop()

    def paint_node_selected(self, node, color=RED):
        node.color = color

    def clear_path(self):
        '''
            apagar caminho da busca anterior
        '''
        self.text_warning = ''
        for edge in self.edges:
            edge.color = edge.no_path_tracking_color

        for node in self.nodes:
            node.color = node.original_color

    def cache_enqueue_selected_nodes(self, node):
        '''
            Enqueue until two nodes before activate breadth_search between nodes
        '''
        if len(self.enqueue_nodes) == 0:
            self.clear_path()

        self.paint_node_selected(node)

        if len(self.enqueue_nodes) == 0 or self.enqueue_nodes[0] != node:
            self.enqueue_nodes.append(node)
        for node in self.enqueue_nodes:
            print(node.value, end=", ")
        print()
        if len(self.enqueue_nodes) >= 2:
            self.search_algorithm_current(
                self.graph, self.enqueue_nodes[0], self.enqueue_nodes[1])
            self.enqueue_nodes = []

    def selected_node(self, position):
        psx = position[0]
        psy = position[1]
        for node in self.nodes:
            radius = NODE_RADIUS
            if (psx > node.posX - radius and psx < node.posX + radius and
                    psy > node.posY - radius and psy < node.posY + radius):
                return node
        return None

    def change_nodes_pos(self, change_posX, change_posY):
        for node in self.nodes:
            node.posX += change_posX
            node.posY += change_posY

    def change_node_pos(self, node, change_posX, change_posY):
        node.posX += change_posX
        node.posY += change_posY

    def set_warning(self, text):
        self.text_warning = text
