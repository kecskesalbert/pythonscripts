#!/usr/bin/env python

class Graph:
    
    def __init__(self, num_nodes = 0):
        self.connections = []
        self.node_in_use = []
        self.num_nodes = num_nodes
        
    def __str__(self):
        pass

    def is_node_connected(self, node):
        if self.node_in_use[node] == 1:
            return False
        is_connected = False
        self.node_in_use[node] = 1
        for idx in range(self.num_nodes):
            if self.connections[node][idx] == 1:
                self.connections[node][idx] = 0
                is_connected = True
                self.is_node_connected(idx)
            if self.connections[idx][node] == 1:
                self.connections[idx][node] = 0
                is_connected = True
                self.is_node_connected(idx)
        return is_connected

    def count_connected(self, num_nodes, edges):
        self.__init__(num_nodes)
        for idx in range(num_nodes):
            self.node_in_use.append(0)
            emptylist = []
            for idy in range(num_nodes):
                emptylist.append(0)
            self.connections.append(emptylist)
        for edge in edges:
            self.connections[edge[0]][edge[1]] = 1
            self.connections[edge[1]][edge[0]] = 1
        cc = 0
        for node in range(num_nodes):
            if (self.is_node_connected(node)):
                cc += 1
        return cc

if __name__ == "__main__":
    graph = Graph()
    print(graph.count_connected(7, [[0, 1], [1, 2], [1, 3], [2, 4], [5, 6]]))
    # print(graph.count_connected(10, [[0, 1], [7, 8], [3, 9], [5, 6], [2, 4], [1, 3], [7, 1], [6, 2]]))
