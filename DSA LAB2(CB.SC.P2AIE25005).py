class DisjointSet:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u != root_v:
            if self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            elif self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1


def kruskal(n, edges):
    
    edges.sort(key=lambda x: x[2])

    ds = DisjointSet(n)
    mst = []
    total_weight = 0

    for u, v, w in edges:
        if ds.find(u - 1) != ds.find(v - 1): 
            ds.union(u - 1, v - 1)
            mst.append((u, v, w))
            total_weight += w

    return total_weight, mst



if __name__ == "__main__":
    n = 4  
    edges = [
        (1, 2, 1),
        (2, 3, 2),
        (4, 2, 4),
        (1, 3, 3)
    ]
    print(" EDGES before finding the sort path",'\n', edges)
    total_weight, mst = kruskal(n, edges)

    print("Edges in the Minimum Spanning Tree:")
    for u, v, w in mst:
        print(f"{u} -- {v} == {w}")

    print(f"\nMinimum paving cost: {total_weight}")
