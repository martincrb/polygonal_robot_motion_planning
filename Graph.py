
class Graph:
    def __init__(self):
        self.V = []
        self.E = []
        self.cost = []

    def addVertex(self, vertex):
        self.V.append(vertex)
        self.cost.append(1)

    def addEdge(self, v1, v2):
        self.E.append([v1, v2])

    def addCost(self, edge, cost):
        if edge in self.E:
            idx = self.E.index(edge)
            self.cost[idx] = cost

    def Dijkstra(self, start, goal):
        Q = {}


    def removeVertices(self, points):
        for p in points:
            if p in self.V:
                self.V.remove(p)
            for edge in self.E:
                if p in edge:
                    self.E.remove(edge)