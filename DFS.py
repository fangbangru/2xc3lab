def DFS(G, node1, node2):
    S = [node1]
    marked = {}
    for node in G.adj:
        marked[node] = False
    marked[node1] = True
    while len(S) != 0:
        node = S.pop()
        if node == node2:
            return True
        for v in G.adj[node]:
            if not marked[v]:
                S.append(v)
                marked[v] = True
    return False