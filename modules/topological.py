from copy import deepcopy
from modules.node import Node
from modules.edge import Edge


def depth_first_search(initial_node: Node, count):
    initial_node.visited = True

    count[0] += 1

    for neighbor in initial_node.neighbors:
        if not hasattr(neighbor.node, 'visited') or neighbor.node.visited == False:
            neighbor.node.visited = True
            depth_first_search(neighbor.node, count)

    count[0] += 1
    # print(initial_node.value, 'count: ', count[0])
    initial_node.topological_count = count[0]
    return initial_node


def topological_dfs(initial_node: Node, graph_nodes: list):
    count = [0]
    last_node = depth_first_search(initial_node, count)

    #  restante dos nodes nao visitados
    while False in list(map(lambda node: node.visited, graph_nodes)):
        for node in graph_nodes:
            if node.visited == False:
                last_node = depth_first_search(
                    node, count)
                break
    return last_node


def topological_bfs(initial_node):
    queue = []

    def enqueue(node):
        node.visited = True
        queue.append(node)

    def dequeue():
        queue[0].active = False
        queue[0].topological_count = 0
        return queue.pop(0)

    if initial_node.active:
        enqueue(initial_node)

    while len(queue) > 0:
        current_node = dequeue()
        print(current_node.value)
        for neighbor in current_node.neighbors:
            if not neighbor.node.visited and neighbor.node.active:
                enqueue(neighbor.node)


def topological_bfs_components(nodes):
    def node_count_bigger():
        max_count = max(
            list(map(lambda node: node.topological_count, nodes)))
        for node in nodes:
            if node.topological_count == max_count and node.active:
                return node

    component_count = 0
    while component_count < 5 and False in list(map(lambda node: node.visited, nodes)):
        print("\nComponent %d:" % component_count)
        node = node_count_bigger()
        topological_bfs(node)
        component_count += 1


def reverse(nodes):
    for node in nodes:
        while len(node.neighbors) > 0:
            neighbor = node.neighbors[0]
            if not neighbor.edge.isReverse:
                neighbor.node.add_neighbor(node, neighbor.edge)
                neighbor.edge.isReverse = True
                node.remove_neighbor(neighbor)
            else:
                break
    return nodes


def clear_visited_nodes(nodes):
    for node in nodes:
        node.visited = False
    return nodes


def topological_order(graph, initial_node):
    '''
        Ordenacao Topologica
    '''
    print("\t\t--- Topological Ordering Components ---\n\n")

    # proteger a estrutura original
    graph_nodes = deepcopy(graph.nodes)
    first_node = graph_nodes[initial_node.value]
    print("initial_node: ", first_node.value)

    # primeira etapa: dfs
    last_node = topological_dfs(first_node, graph_nodes)
    print("last: ", last_node.value)

    # segunda etapa: arvore inversa
    graph_nodes = reverse(graph_nodes)

    # terceira etapa: bfs para encontrar os componentes
    graph_nodes = clear_visited_nodes(graph_nodes)
    topological_bfs_components(graph_nodes)
