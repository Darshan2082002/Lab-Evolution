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
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])

    ds = DisjointSet(n)
    mst = []
    total_weight = 0

    for u, v, w in edges:
        if ds.find(u - 1) != ds.find(v - 1):  # adjusting for 1-based input
            ds.union(u - 1, v - 1)
            mst.append((u, v, w))
            total_weight += w

    return total_weight, mst


if __name__ == "__main__":
    print("Kruskals Algorithm - Minimum Spanning Tree\n")

    
    n = int(input("Enter the number of vertices: "))
    e = int(input("Enter the number of edges: "))

    edges = []
    print("\nEnter each edge in the format: source destination weight")
    for i in range(e):
        u, v, w = map(int, input(f"Edge {i+1}: ").split())
        edges.append((u, v, w))

    total_weight, mst = kruskal(n, edges)

    print("\nEdges in the Minimum Spanning Tree:")
    for u, v, w in mst:
        print(f"{u} -- {v} == {w}")

    print(f"\nMinimum paving cost: {total_weight}")
