import pygame
import pygame.gfxdraw
from pygame.locals import *
import random
from math import cos, sin, atan, sqrt, pi
from modules.config import *
from modules.screen_objects import Button
from modules.edge import EdgeDirected


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
        self.node_selected = None

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
            edge.draw(self.screen)

        # Draw Nodes
        for node in self.nodes:
            node_text = self.font.render(str(node.value), True, WHITE)
            pygame.gfxdraw.filled_circle(
                self.screen, node.posX, node.posY, node.radius, node.color)
            self.screen.blit(node_text, (node.txt_posX, node.txt_posY))

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
