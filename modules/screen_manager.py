import pygame
import math
import time
from modules.config import *
from modules.menu_screen import Menu
from modules.graph_screen import GraphScreen
from modules.graph import Graph
from modules.search_methods import breadth_search, depth_first_search
from modules.dijkstra import dijkstra_algorithm


class Screen(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = None
        self.clock = pygame.time.Clock()
        self.menu = None
        self.graph_screen = None
        self.keys_listener_selected = None
        self.draw_screen_selected = None
        self.graph = None

    def start(self):
        pygame.display.set_caption("Graph")
        pygame.init()
        self.font = pygame.font.Font(
            'modules/fonts/roboto/Roboto-Black.ttf', 15)

        # init programm with menu screen
        # self.switch_to_menu()
        self.switch_to_graph()

    def switch_to_menu(self):
        del self.menu
        self.menu = Menu(self.screen, self, self.clock)
        self.keys_listener_selected = self.menu.keys_listener
        self.draw_screen_selected = self.menu.draw

    def switch_to_graph(self, qtt_nodes=10, qtt_edges=10):
        del self.graph
        del self.graph_screen

        self.graph_screen = GraphScreen(self.screen, self, self.clock)
        self.graph = Graph(self.graph_screen)

        self.graph_screen.set_graph(self.graph)
        self.graph_screen.set_generate_graph(
            self.graph.automatic_generation_graph)
        self.graph_screen.set_search_algorithm(
            breadth_search, depth_first_search)
        self.graph_screen.set_dijkstra_algorithm(dijkstra_algorithm)

        self.graph_screen.start(qtt_nodes, qtt_edges)
        self.keys_listener_selected = self.graph_screen.keys_listener
        self.draw_screen_selected = self.graph_screen.draw

    def refresh(self):
        while 1:
            self.keys_listener_selected()
            self.draw_screen_selected()
