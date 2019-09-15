'''
    File with Dijkstra algorithm
'''
from copy import deepcopy
from modules.node import Node
from modules.heap import HeapDijkstra


def start_heap(first_node, graph_nodes):
    heap_nodes = []
    for node in graph_nodes:
        if node != first_node:
            heap_nodes.append([None, node, None, None])
        else:
            heap_nodes.append([0, node, None, None])

    heap = HeapDijkstra(heap_nodes)
    return heap


def update_edge_neighbors(heap_node, heap):
    '''
        structure heap_node: (lengh, dest_node, origin_node, edge_between)
    '''
    for neighbor in heap_node[1].neighbors:
        path_lenght = heap_node[0] + neighbor.edge.lenght
        heap.update_node_lenght(
            neighbor.node, heap_node[1], path_lenght, neighbor.edge)


def add_child_tree(parent_node, child_node, edge):
    '''
        arvore temporaria para salvar o caminho de volta para a raiz
    '''
    parent_node.childs.append(child_node)

    child_node.parent.edge = edge
    child_node.parent.node = parent_node


def prepare_to_tree(nodes):
    for node in nodes:
        node.childs = []
        node.parent = type('', (), {})()


def dijkstra_algorithm(graph, initial_node, end_node):
    '''
        Algoritmo dijkstra de menor caminho em grafos com pesos
    '''
    # proteger a estrutura original
    graph_nodes = deepcopy(graph.nodes)
    first_node = graph_nodes[initial_node.value]
    dest_node = graph_nodes[end_node.value]

    prepare_to_tree(graph_nodes)

    # heap para priorizar o menor caminho
    heap = start_heap(first_node, graph_nodes)
    heap.show_nodes()

    while True:
        heap_root = heap.get_root()
        # print(heap_root[1].value, end=", ")
        # paint edge and add on tree backtrack
        if heap_root[3]:
            graph.paint_tracking_edges(
                heap_root[3], heap_root[1], heap_root[2])
            add_child_tree(heap_root[2], heap_root[1], heap_root[3])
        # desenha caminho de busca
        if heap_root[1] == dest_node:
            break
        update_edge_neighbors(heap_root, heap)
        # heap.show_nodes()

    # end
    print("distance %s, origin %s -> end %s" %
          (heap_root[0], first_node.value, dest_node.value))
    # paint path until root of tree
    graph.paint_tracked_edges(heap_root[1])
    graph.change_color_node(
        initial_node, Node.path_tracked_color)
    graph.change_color_node(
        end_node, Node.path_tracked_color)
