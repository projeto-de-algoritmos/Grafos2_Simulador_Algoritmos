from copy import deepcopy
import random
from modules.config import *
from modules.node import Node
from modules.edge import Edge, EdgeDirected


class Graph(object):
    def __init__(self, screen):
        self.screen = screen
        self.edge_type: int = 0
        self.nodes = []
        self.edges = []
        self.array_nodes_posX = []
        self.array_nodes_posY = []

    def __set_positions(self):
        ''''
            add positions preventing colisions
        '''
        MIN_DISTANCE_BETWEEN_NODES = NODE_RADIUS * 3
        posValid = False
        while posValid != True:
            posX = random.randint(
                NODE_RADIUS, SCREEN_WIDTH - NODE_RADIUS)
            posY = random.randint(
                NODE_RADIUS, SCREEN_HEIGHT - NODE_RADIUS)

            # verify positions
            invalid = False
            for (pX, pY) in zip(self.array_nodes_posX, self.array_nodes_posY):
                if abs(pX - posX) < MIN_DISTANCE_BETWEEN_NODES and abs(pY - posY) < MIN_DISTANCE_BETWEEN_NODES:
                    invalid = True
                    break
            if invalid == False:
                posValid = True
        # add occupied positions
        self.array_nodes_posX.append(posX)
        self.array_nodes_posY.append(posY)
        return (posX, posY)

    def set_edge_type(self, edge_type):
        self.edge_type = edge_type

    def create_nodes(self, values=[]):
        nodes = []
        for value in values:
            nodes.append(Node(value))
        self.make_nodes_screen(nodes)
        self.nodes.extend(nodes)
        return nodes

    def make_nodes_screen(self, nodes: list):
        for node in nodes:
            node.original_color = DARK_GRAY
            node.posX, node.posY = self.__set_positions()
            self.screen.create_node(node)

    def create_relationship(self, node, nodes: list):
        neighbors = nodes

        for neighbor in neighbors:
            edge = Edge()
            edge = self.__make_edge_screen(node, neighbor, edge)
            node.add_neighbor(neighbor, edge)
            neighbor.add_neighbor(node, edge)
            self.edges.append(edge)

        return neighbors

    def create_relationship_directed(self, node, nodes: list):
        neighbors = nodes

        for neighbor in neighbors:
            edge = EdgeDirected()
            edge = self.__make_edge_screen(node, neighbor, edge)
            node.add_neighbor(neighbor, edge)
            self.edges.append(edge)

        return neighbors

    def __make_edge_screen(self, node1, node2, edge, color=Edge.no_path_tracking_color):
        edge.node_start = node1
        edge.node_end = node2
        edge.color = color
        self.screen.add_edge(edge)
        return edge

    def change_color_node(self, node, color):
        '''
            Funcao para alterar a cor de um node no graph original
        '''
        node_select = self.nodes[node.value]
        node_select.color = color

    def __change_color_edge(self, edge, color):
        '''
            Funcao para alterar a cor de uma edge no graph original
        '''
        edge_select = self.edges[edge.value]
        edge_select.color = color

    def paint_tracked_edges(self, child_node):
        '''
            Funcao para pintar o caminho do node filho ate o node pai,
            utilizando a arvore gerada pela breadth_search
        '''
        if hasattr(child_node.parent, 'edge') and hasattr(child_node.parent, 'node'):
            self.paint_tracked_edges(child_node.parent.node)
            self.__change_color_edge(
                child_node.parent.edge, child_node.parent.edge.path_tracked_color)
            if len(child_node.childs) > 0:
                self.change_color_node(
                    child_node, child_node.path_tracked_middle_color)
            self.screen.draw(3)

    def __make_temp_edge_screen(self, node1_pos: tuple, node2_pos: tuple, color=Edge.no_path_tracking_color):
        edge = Edge()
        edge.start = node1_pos
        edge.end = node2_pos
        edge.color = color
        self.screen.add_edge(edge)
        return edge

    def paint_tracking_edges(self, edge, node1, node2, color_index=0):
        '''
            Pintar o caminho de busca do node
        '''
        color = [(edge.path_tracking_color, node2.path_tracking_color),
                 (edge.path_tracked_color, node2.path_tracked_middle_color)]
        self.__change_color_edge(edge, color[color_index][0])
        self.change_color_node(node2, color[color_index][1])
        self.screen.draw(3)

    def __return_random_nodes(self, node, qtt_average, qtt_edges_remainder):
        '''
            Retorna uma lista de nodes aleatoriamente
        '''
        max_neighbors = len(self.nodes) - 1
        max_size = max_neighbors if max_neighbors < qtt_edges_remainder else qtt_edges_remainder

        if qtt_average is 0:
            qtt_average = max_size
        size_list = random.randint(0, qtt_average)
        array_nodes = []

        # neighbors already exists
        neighbor_already = []
        for neighbor in node.neighbors:
            neighbor_already.append(neighbor.node)

        for n in range(size_list):
            while True:
                # node escolhido da lista nao pode ser ele mesmo e nem ser repetido
                node_picked = self.nodes[random.randint(
                    0, len(self.nodes) - 1)]
                if (node_picked != node and node_picked not in (array_nodes) and
                        node_picked not in neighbor_already):
                    break

            array_nodes.append(node_picked)
        return array_nodes

    def __automatic_generation_edges(self, nodes: list, qtt_edges):
        qtt_edges_remainder = qtt_edges
        qtt_average = int(qtt_edges/len(self.nodes))
        qtt_nodes = len(nodes)
        index_node = 0
        while qtt_edges_remainder > 0:
            node = nodes[index_node]
            neighbors = self.__return_random_nodes(
                node, qtt_average, qtt_edges_remainder)
            qtt_edges_remainder -= len(neighbors)
            if self.edge_type == 0:
                self.create_relationship(node, neighbors)
            else:
                self.create_relationship_directed(node, neighbors)
            index_node = (index_node + 1) % (qtt_nodes)

    def automatic_generation_graph(self, qtt_nodes: int, qtt_edges: int):
        Node.indexes_used = []
        Edge.index = 0
        del self.nodes
        del self.edges
        self.nodes = []
        self.edges = []
        max_edges = int((qtt_nodes*(qtt_nodes - 1)) / 2)

        values = []
        nodes = []
        for n in range(qtt_nodes):
            values.append(n)

        nodes = self.create_nodes(values)
        self.__automatic_generation_edges(nodes, qtt_edges)
