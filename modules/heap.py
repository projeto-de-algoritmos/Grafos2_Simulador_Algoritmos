import math


class HeapDijkstra(object):
    def __init__(self, nodes: list = []):
        '''
            structure node: (edge_lengh, destination_node, origin_node)
        '''
        self.nodes = [None]

        self.__start_heap(nodes)

    def __start_heap(self, nodes: list = []):
        for node in nodes:
            self.add_node(node)

    def show_nodes(self):
        nodes = self.nodes
        print('Heap Nodes:')
        print('[', end='')
        for index in range(1, len(nodes)):
            if index < len(nodes) - 1:
                print('(%s, %s, %s)' % (
                    nodes[index][0], nodes[index][1].value,
                    nodes[index][2].value if nodes[index][2] else None), end=',\n')
            else:
                print('(%s, %s, %s)' % (
                    nodes[index][0], nodes[index][1].value,
                    nodes[index][2].value if nodes[index][2] else None), end='')
        print(']\n')

    def add_node(self, node):
        position_index = len(self.nodes)
        self.nodes.append(node)
        self.__shift_up(node, position_index)

    def update_node_lenght(self, node, new_origin_node, new_lenght):
        '''
            atualiza o custo do caminho ate o node se for menor que o custo atual
            arg node eh o dest_node
        '''
        for index in range(1, len(self.nodes)):
            if self.nodes[index][1] == node:
                if self.nodes[index][0] == None or new_lenght < self.nodes[index][0]:
                    self.nodes[index][0] = new_lenght
                    self.nodes[index][2] = new_origin_node
                    self.__shift_up(self.nodes[index], index)
                return

    def get_root(self):
        '''
            return destination_root
        '''
        node = self.remove_root()
        return node

    def remove_root(self):
        position_last = len(self.nodes) - 1
        position_root = 1
        if position_last <= 0:
            return
        last_node = self.nodes[position_last]
        root_node = self.nodes[position_root]

        self.nodes[position_root] = last_node
        self.nodes.pop(len(self.nodes) - 1)
        self.__shift_down(last_node, position_root)
        return root_node

    def __shift_up(self, node, position_node):
        position_parent = math.floor(position_node/2)
        if position_parent <= 0:
            return
        parent_node = self.nodes[position_parent]

        if ((parent_node[0] == None and node[0] != None) or
                (parent_node[0] != None and node[0] != None and node[0] < parent_node[0])):
            self.nodes[position_parent] = node
            self.nodes[position_node] = parent_node

            self.__shift_up(node, position_parent)

    def __shift_down(self, node, position_node):
        position_left_child = position_node * 2
        position_right_child = position_node * 2 + 1
        if position_left_child <= len(self.nodes) - 1:
            left_child_node = self.nodes[position_left_child]
        else:
            return
        if position_right_child <= len(self.nodes) - 1:
            right_child_node = self.nodes[position_right_child]
        else:
            return

        small_node = node
        position_small = position_node
        small_changed = False

        if (small_node[0] == None and left_child_node[0] != None or
            (left_child_node[0] != None and small_node[0] != None and
             left_child_node[0] < small_node[0])):

            small_node = left_child_node
            position_small = position_left_child
            small_changed = True
        if (small_node[0] == None and right_child_node[0] != None or
            (right_child_node[0] != None and small_node[0] != None and
             right_child_node[0] < small_node[0])):

            small_node = right_child_node
            position_small = position_right_child
            small_changed = True

        if small_changed:
            self.nodes[position_node] = small_node
            self.nodes[position_small] = node

            self.__shift_down(node, position_small)
