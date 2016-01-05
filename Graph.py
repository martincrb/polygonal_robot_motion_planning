
class Graph:
    def __init__(self):
        self.V = []
        self.E = []

    def addVertex(self, vertex):
        self.V.append(vertex)

    def addEdge(self, v1, v2):
        self.E.append([v1, v2])

    def removeVertices(self, points):
        for p in points:
            if p in self.V:
                self.V.remove(p)
            for edge in self.E:
                if p in edge:
                    self.E.remove(edge)