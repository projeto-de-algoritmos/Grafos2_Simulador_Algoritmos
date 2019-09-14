from copy import deepcopy
from modules.node import Node


def add_child_tree(parent_node, child_node, edge):
    '''
        arvore temporaria para salvar o melhor caminho do initial_node para end_node
    '''
    parent_node.childs.append(child_node)

    child_node.parent.edge = edge
    child_node.parent.node = parent_node


def breadth_search(graph, initial_node: Node, end_node: Node):
    queue = []

    def enqueue(node):
        node.visited = True
        # atributos para usar na arovore temporaria
        node.childs = []
        node.parent = type('', (), {})()
        queue.append(node)

    def dequeue():
        return queue.pop(0)

    # realiza uma copia, para nao afetar a variavel original
    node = deepcopy(initial_node)

    # realiza busca em largura dos nodes alcancaveis a partir do node principal
    enqueue(node)

    while len(queue) > 0:
        current_node = dequeue()

        for neighbor in current_node.neighbors:
            if not hasattr(neighbor.node, 'visited') or neighbor.node.visited == False:
                enqueue(neighbor.node)
                # desenha caminho de busca
                graph.paint_tracking_edges(
                    neighbor.edge, current_node, neighbor.node)
                # adiciona nodes vizinhos como filhos do node da camada anterior
                add_child_tree(
                    current_node, neighbor.node, neighbor.edge)

                # verificar se eh o node procurado
                if neighbor.node.value == end_node.value:
                    graph.change_color_node(
                        initial_node, Node.path_tracked_color)
                    graph.change_color_node(
                        end_node, Node.path_tracked_color)
                    graph.paint_tracked_edges(neighbor.node)
                    return
        if len(queue) == 0:
            graph.screen.set_warning('Impossivel ligar os dois Vertices')
            return


def depth_first_search(graph, initial_node: Node, end_node: Node):
    '''
        Funcao auxiliar a depth first recursion, para desenhar o caminho original
    '''
    node_start = deepcopy(initial_node)
    node_end = deepcopy(end_node)

    result = depth_first_search_recursion(graph, node_start, node_end)
    if result != None:
        graph.change_color_node(
            initial_node, Node.path_tracked_color)
        graph.change_color_node(
            end_node, Node.path_tracked_color)
    else:
        graph.screen.set_warning('Impossivel ligar os dois Vertices')
    return


def depth_first_search_recursion(graph, initial_node: Node, end_node: Node):
    node = initial_node

    node.visited = True
    node.parent = type('', (), {})()
    node.childs = []

    for neighbor in node.neighbors:
        neighbor.node.parent = type('', (), {})()
        neighbor.node.childs = []
        if not hasattr(neighbor.node, 'visited') or neighbor.node.visited == False:
            neighbor.node.visited = True
            # desenha caminho de busca
            graph.paint_tracking_edges(
                neighbor.edge, node, neighbor.node, 1)
            # arvore de busca
            add_child_tree(
                node, neighbor.node, neighbor.edge)

            # verificar se eh o node procurado
            if neighbor.node.value == end_node.value:
                    # retorna o node procurado com a arvore
                return node

            result = depth_first_search_recursion(
                graph, neighbor.node, end_node)

            if result != None:
                node = result
                return node
            else:
                graph.paint_tracking_edges(
                    neighbor.edge, node, neighbor.node, 0)
