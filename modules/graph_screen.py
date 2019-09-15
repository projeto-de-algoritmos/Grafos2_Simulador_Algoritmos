import pygame
import pygame.gfxdraw
from pygame.locals import *
import random
from math import cos, sin, atan, sqrt, pi
from modules.config import *
from modules.screen_objects import Button


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
        self.search_bfs = None
        self.search_dfs = None
        self.algorithm_current = None
        self.dijkstra_algorithm = None
        self.topological_algorithm = None
        self.generate_graph = None
        self.edge_weight = True
        self.show_edge_dir = False

        # objects
        self.label_warning = None
        self.button_menu = Button('Menu', 20, SCREEN_HEIGHT - 50)
        self.button_topological = Button(
            'TOP', SCREEN_WIDTH - 300, SCREEN_HEIGHT - 50)
        self.button_topological.set_colors(RED, LIGHT_RED)
        self.button_type_bfs = Button(
            'BFS', SCREEN_WIDTH - 220, SCREEN_HEIGHT - 50)
        self.button_type_dfs = Button(
            'DFS', SCREEN_WIDTH - 160, SCREEN_HEIGHT - 50)
        self.button_type_dijkstra = Button(
            'Dijkstra', SCREEN_WIDTH - 100, SCREEN_HEIGHT - 50)

        self.button_current_algorithm = None
        self.node_selected = None

    def start(self, qtt_nodes, qtt_edges):
        self.nodes = []
        self.edges = []
        self.button_type_bfs.clicked()
        self.button_current_algorithm = self.button_type_bfs
        self.generate_graph(qtt_nodes, qtt_edges)

    def set_graph(self, graph):
        self.graph = graph

    def set_generate_graph(self, generate_graph):
        self.generate_graph = generate_graph

    def set_search_algorithm(self, search_bfs=None, search_dfs=None):
        self.search_bfs = search_bfs
        self.search_dfs = search_dfs
        self.algorithm_current = search_bfs

    def set_dijkstra_algorithm(self, dijkstra):
        self.dijkstra_algorithm = dijkstra

    def set_topological(self, topological):
        self.topological_algorithm = topological

    def set_algorithm_current(self, search_algorithm):
        self.algorithm_current = search_algorithm

    def set_show_edge_dir(self, edge_type):
        self.show_edge_dir = edge_type

    def disable_edge_weight(self):
        self.edge_weight = False

    def draw(self, clock_fps=30):
        # redraw screen
        self.screen.fill(LIGHT_GRAY)
        # Draw edges
        for edge in self.edges:
            edge.draw(self.screen, self.font)

        # Draw Nodes
        for node in self.nodes:
            node_text = self.font.render(str(node.value), True, WHITE)
            pygame.gfxdraw.filled_circle(
                self.screen, node.posX, node.posY, node.radius, node.color)
            self.screen.blit(node_text, (node.txt_posX, node.txt_posY))

        # Draw Buttons
        self.button_menu.draw(self.screen)
        self.button_topological.draw(self.screen)
        self.button_type_bfs.draw(self.screen)
        self.button_type_dfs.draw(self.screen)
        self.button_type_dijkstra.draw(self.screen)

        # render warning
        if self.label_warning:
            self.screen.blit(self.label_warning,
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
                    # pressed on right button and moving
                    # move all nodes
                    rel = event.rel
                    self.change_nodes_pos(rel[0], rel[1])
                if event.buttons[0]:
                    # pressed on left button to drag node
                    # move one node
                    position = pygame.mouse.get_pos()
                    if self.node_selected is None:
                        self.node_selected = self.selected_node(position)
                    if self.node_selected is not None:
                        rel = event.rel
                        self.change_node_pos(
                            self.node_selected, rel[0], rel[1])

            elif event.type == pygame.MOUSEBUTTONUP:
                # if left button is clicked on node
                position = pygame.mouse.get_pos()
                node = self.selected_node(position)
                if node is not None and self.node_selected is None:
                    self.cache_enqueue_selected_nodes(node)
                else:
                    self.node_selected = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                # if clicked on Button Menu
                if self.button_menu.box.collidepoint(event.pos):
                    self.button_menu.clicked()
                    self.screen_manager.switch_to_menu()

                # select topological order
                if (self.button_topological.box.collidepoint(event.pos) and
                        self.topological_algorithm and self.show_edge_dir):
                    # prevent error with node already selected
                    self.enqueue_nodes = []
                    self.clear_path()
                    if self.button_topological.active is False:
                        self.button_topological.clicked()
                        self.button_current_algorithm.clicked()
                        self.button_current_algorithm = self.button_topological

                        # set algorithm
                        self.set_algorithm_current(
                            self.topological_algorithm)

                if self.button_type_bfs.box.collidepoint(event.pos) and self.search_bfs:
                    if self.button_type_bfs.active is False:
                        self.button_type_bfs.clicked()
                        self.button_current_algorithm.clicked()
                        self.button_current_algorithm = self.button_type_bfs

                        # set algorithm
                        self.set_algorithm_current(
                            self.search_bfs)

                if self.button_type_dfs.box.collidepoint(event.pos) and self.search_dfs:
                    if self.button_type_dfs.active is False:
                        self.button_type_dfs.clicked()
                        self.button_current_algorithm.clicked()
                        self.button_current_algorithm = self.button_type_dfs

                        # set algorithm
                        self.set_algorithm_current(
                            self.search_dfs)

                if self.button_type_dijkstra.box.collidepoint(event.pos) and self.dijkstra_algorithm and self.edge_weight:
                    if self.button_type_dijkstra.active is False:
                        self.button_type_dijkstra.clicked()
                        self.button_current_algorithm.clicked()
                        self.button_current_algorithm = self.button_type_dijkstra

                        # set algorithm
                        self.set_algorithm_current(
                            self.dijkstra_algorithm)

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
        self.set_warning('')
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
        if len(self.enqueue_nodes) == 1 and self.algorithm_current == self.topological_algorithm:
            self.algorithm_current(
                self.graph, self.enqueue_nodes[0])
            self.enqueue_nodes = []
        if len(self.enqueue_nodes) >= 2:
            self.algorithm_current(
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

    def set_warning(self, text, color=RED):
        self.label_warning = self.font.render(text, True, color)
