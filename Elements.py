#Basic polygon class
import pygame

class Element:
    #The vertices are relative to (0,0). We must add the (x,y) when drawing
    def __init__(self):
        self.vertices = []
        self.color = (0,0,0)
        self.point_color = (0,0,255)
        self.viewPoints = True

    def addVertex(self, vertex):
        self.vertices.append(vertex)

    def draw(self, surface):
        #final_points = map(lambda x: x + (self.x, self.y), self.vertices)
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

class Obstacle(Element):

    def __init__(self):
        self.vertices = []
        self.color = (128,128,128)
        self.point_color = (0,0,255)
        self.viewPoints = True

class Robot(Element):

    def __init__(self):
        self.vertices = []
        self.color = (255,0,0)
        self.point_color = (0,255,0)
        self.viewPoints = True

class Target(Element):

    def __init__(self):
        self.vertices = []
        self.color = (0,255,0)
        self.point_color = (0,255,0)
        self.viewPoints = True

    def setVertex(self, vertex):
        self.vertices = [vertex]