'''
    File with Dijkstra algorithm
'''
from copy import deepcopy
from modules.heap import HeapDijkstra


def update_edge_neighbors(heap_node, heap):
    '''
        estrutura heap_node: (lengh, dest_node, origin_node)
    '''
    for neighbor in heap_node[1].neighbors:
        path_lenght = heap_node[0] + neighbor.edge.lenght
        heap.update_node_lenght(neighbor.node, heap_node[1], path_lenght)


def start_heap(first_node, graph_nodes):
    heap_nodes = []
    for node in graph_nodes:
        if node != first_node:
            heap_nodes.append([None, node, None])
        else:
            heap_nodes.append([0, node, None])

    heap = HeapDijkstra(heap_nodes)
    return heap


def dijkstra_algorithm(graph, initial_node, end_node):
    '''
        Algoritmo dijkstra de menor caminho em grafos com pesos
    '''
    nodes = graph.nodes
    # proteger a estrutura original
    graph_nodes = deepcopy(nodes)
    first_node = graph_nodes[initial_node.value]
    dest_node = graph_nodes[end_node.value]

    # heap para priorizar o menor caminho
    heap = start_heap(first_node, graph_nodes)
    # heap.show_nodes()

    print("Caminho:")
    while True:
        heap_root = heap.get_root()
        print(heap_root[1].value, end=", ")
        if heap_root[1] == dest_node:
            break
        update_edge_neighbors(heap_root, heap)
        # heap.show_nodes()
    print()

    print("distance %s, origin %s -> end %s" %
          (heap_root[0], heap_root[2].value, heap_root[1].value))
