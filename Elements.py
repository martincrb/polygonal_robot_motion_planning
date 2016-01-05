#Basic polygon class
import pygame
import math

class Element:
    #The vertices are relative to (0,0). We must add the (x,y) when drawing
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.color = (0,0,0)
        self.point_color = (0,0,255)
        self.viewPoints = True

    def contains_point(self, p):
        return p in self.vertices

    def contains_edge(self, p, q):
        return [p,q] in self.edges

    def addVertex(self, vertex):
        self.vertices.append(vertex)
        self.edges = []
        if (len(self.vertices) >= 2):
            for i in range(1, len(self.vertices)):
                self.edges.append([self.vertices[i-1], self.vertices[i]])
        self.edges.append([self.vertices[len(self.vertices)-1], self.vertices[0]])

    def draw(self, surface):
        if len(self.vertices) > 2:
            pygame.draw.polygon(surface, self.color, self.vertices)
        elif len(self.vertices) == 1:
            for vertex in self.vertices:
                pygame.draw.circle(surface, self.point_color, vertex, 1)
        elif len(self.vertices) == 2:
            pygame.draw.line(surface, self.color, self.vertices[0], self.vertices[1])
            for vertex in self.vertices:
                pygame.draw.circle(surface, self.point_color, vertex, 1)
        if self.viewPoints:
            for vertex in self.vertices:
                pygame.draw.circle(surface, self.point_color, vertex, 1)

        #for e in self.edges:
        #    pygame.draw.line(surface, self.color, e[0], e[1])

    def getVertices(self):
        return self.vertices

    def setVertices(self, vertices):
        self.vertices = vertices
        if (len(self.vertices) >= 2):
            for i in range(1, len(self.vertices)):
                self.edges.append([self.vertices[i-1], self.vertices[i]])
        self.edges.append([self.vertices[len(self.vertices)-1], self.vertices[0]])

class Obstacle(Element):

    def __init__(self):
        self.vertices = []
        self.edges = []
        self.color = (128,128,128)
        self.point_color = (0,0,255)
        self.viewPoints = True

class C_Obstacle(Element):

    def __init__(self):
        self.vertices = []
        self.edges = []
        self.color = (180,180,180)
        self.point_color = (0,0,220)
        self.viewPoints = True

class Robot(Element):

    def __init__(self):
        self.vertices = []
        self.edges = []
        self.color = (255,0,0)
        self.point_color = (0,255,0)
        self.viewPoints = True

    def getRefPoint(self):
        if (len(self.vertices) > 0):
            return self.vertices[0]

class Target(Element):

    def __init__(self):
        self.vertices = []
        self.edges = []
        self.color = (0,255,0)
        self.point_color = (0,255,0)
        self.viewPoints = True

    def setVertex(self, vertex):
        self.vertices = [vertex]