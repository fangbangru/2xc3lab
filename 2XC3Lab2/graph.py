import random
from collections import deque

#Undirected graph using an adjacency list
class Graph:

    def __init__(self, n):
        self.adj = {}
        for i in range(n):
            self.adj[i] = []

    def are_connected(self, node1, node2):
        return node2 in self.adj[node1]

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self):
        self.adj[len(self.adj)] = []

    def add_edge(self, node1, node2):
        if node1 == node2:
            return
        if node1 not in self.adj[node2]:
            self.adj[node1].append(node2)
            self.adj[node2].append(node1)

    def number_of_nodes(self):
        return len(self.adj)
    
    def get_size(self):
        return len(self.adj)


#Breadth First Search
def BFS(G, node1, node2):
    Q = deque([node1])
    marked = {node1 : True}
    for node in G.adj:
        if node != node1:
            marked[node] = False
    while len(Q) != 0:
        current_node = Q.popleft()
        for node in G.adj[current_node]:
            if node == node2:
                return True
            if not marked[node]:
                Q.append(node)
                marked[node] = True
    return False

def BFS2(G, node1, node2):
    if node1 == node2:
        return [node1]

    Q = deque([node1])
    visited = {node1}
    pred = {} 

    while Q:
        u = Q.popleft()
        for v in G.adj[u]:
            if v not in visited:
                visited.add(v)
                pred[v] = u
                if v == node2:
                    path = [node2]
                    cur = node2
                    while cur != node1:
                        cur = pred[cur]
                        path.append(cur)
                    path.reverse()
                    return path
                Q.append(v)

    return []  # not found

def BFS3(G, start):
    Q = deque([start])
    visited = {start}
    pred = {} 

    while Q:
        u = Q.popleft()
        for v in G.adj[u]:
            if v not in visited:
                visited.add(v)
                pred[v] = u
                Q.append(v)

    return pred

#Depth First Search
def DFS(G, node1, node2):
    S = [node1]
    marked = {}
    for node in G.adj:
        marked[node] = False
    while len(S) != 0:
        current_node = S.pop()
        if not marked[current_node]:
            marked[current_node] = True
            for node in G.adj[current_node]:
                if node == node2:
                    return True
                S.append(node)
    return False

def DFS2(G, node1, node2):
    if node1 == node2:
        return [node1]

    S = [node1]
    visited = {node1}
    pred = {}

    while S:
        u = S.pop()
        if u == node2:
            break

        for v in G.adj[u]:
            if v not in visited:
                visited.add(v)
                pred[v] = u
                S.append(v)

    if node2 not in visited:
        return []

    path = [node2]
    cur = node2
    while cur != node1:
        cur = pred[cur]
        path.append(cur)
    path.reverse()
    return path

def DFS3(G, start):
    S = [start]
    visited = {start}
    pred = {}

    while S:
        u = S.pop()
        for v in G.adj[u]:
            if v not in visited:
                visited.add(v)
                pred[v] = u
                S.append(v)

    return pred

def is_connected(G):
    n = len(G.adj)
    if n <= 1:
        return True

    start = next(iter(G.adj))  
    pred = BFS3(G, start)
    reachable = 1 + len(pred)  
    return reachable == n

#has_cycle
def has_cycle(G):
    visited = set()

    def dfs(u, parent):
        visited.add(u)
        for v in G.adj[u]:
            if v not in visited:
                if dfs(v, u):
                    return True
            elif v != parent:
                return True
        return False

    for node in G.adj:
        if node not in visited:
            if dfs(node, -1):
                return True
    return False

def create_random_graph(i, j):
    max_edges = i * (i - 1) // 2
    if j > max_edges:
        raise ValueError(f"Too many edges: j={j} > {max_edges} for i={i}")

    G = Graph(i)
    edges = set()

    while len(edges) < j:
        u = random.randrange(i)
        v = random.randrange(i)
        if u == v:
            continue
        a, b = (u, v) if u < v else (v, u)
        if (a, b) in edges:
            continue
        edges.add((a, b))
        G.add_edge(a, b)

    return G

#Use the methods below to determine minimum vertex covers

def add_to_each(sets, element):
    copy = sets.copy()
    for set in copy:
        set.append(element)
    return copy

def power_set(set):
    if set == []:
        return [[]]
    return power_set(set[1:]) + add_to_each(power_set(set[1:]), set[0])

def is_vertex_cover(G, C):
    for start in G.adj:
        for end in G.adj[start]:
            if not(start in C or end in C):
                return False
    return True

def MVC(G):
    nodes = [i for i in range(G.get_size())]
    subsets = power_set(nodes)
    min_cover = nodes
    for subset in subsets:
        if is_vertex_cover(G, subset):
            if len(subset) < len(min_cover):
                min_cover = subset
    return min_cover



