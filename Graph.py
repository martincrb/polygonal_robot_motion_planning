from pythonds.graphs import PriorityQueue

class Graph:
    def __init__(self):
        self.V = []
        self.E = []
        self.cost = {}
        self.neighbours = {}

    def addVertex(self, vertex):
        self.V.append(vertex)
        self.cost[vertex] = 1
        self.neighbours[vertex] = []

    def addEdge(self, v1, v2):
        self.E.append((v1, v2))
        self.neighbours[v1].append(v2)

    def addCost(self, edge, cost):
        if edge in self.E:
            self.cost[edge] = cost

    def getCost(self, edge):
        if edge in self.E:
            return self.cost[edge]

    def getNeighbors(self, vertex):
        if vertex in self.V:
            return self.neighbours[vertex]

    def DijkstraShortestPath(self, start, goal):
        Q = set()
        distances = {}
        prev = {}
        for v in self.V:
            distances[v] = float("inf")
            prev[v] = None
            Q.add((v[0], v[1]))

        distances[start] = 0
        while Q:
            u = min(Q, key=distances.get)
            if u == goal:
                break
            Q.remove(u)
            for v in self.getNeighbors(u):
                c = distances[u] + self.cost[(u,v)]
                if c < distances[v]:
                    distances[v] = c
                    prev[v] = u

        path = []
        u = goal
        while prev[u] != None:
            path.append(u)
            u = prev[u]
        path.append(u)
        return path[::-1]

    def removeVertices(self, points):
        for p in points:
            if p in self.V:
                self.V.remove(p)
            for edge in self.E:
                if p in edge:
                    self.E.remove(edge)