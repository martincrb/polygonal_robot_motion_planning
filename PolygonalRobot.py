import pygame
import time
from Elements import *
from State import *
from VisibilityGraph import *

#Start main window
dimensions = (800, 600)
screen = pygame.display.set_mode(dimensions)
pygame.display.set_caption('Polygonal Robot: motion planning')
background_colour = (255,255,255)
clock = pygame.time.Clock()
running = True
debug = False
elapsed_time = None
#fonts
pygame.font.init()
font = pygame.font.SysFont("monospace", 15)



#logic elements
obstacles = []
c_obstacles = []
robot = None
minus_robot = None
target = None
path = []
pathEdges = []
#define global state of application
states = State()
(V, E) = (None, None)
while running:
    #Read and process user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mousex, mousey) = pygame.mouse.get_pos()
            if states.getActualState() == "DRAWING_OBSTACLE":
                obstacles[len(obstacles) - 1].addVertex((mousex, mousey))
            if states.getActualState() == "DRAWING_ROBOT":
                robot.addVertex((mousex, mousey))
            if states.getActualState() == "SELECT_TARGET":
                print "Target selected"
                target.setVertex((mousex, mousey))
                states.setActualState(None)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                if states.getActualState() == "DRAWING_OBSTACLE":
                    print "Finish drawing obstacle"
                    states.setActualState(None)
                else:
                    print "Started drawing obstacle"
                    states.setActualState("DRAWING_OBSTACLE")
                    #create empty polygon and append to obstacles list
                    obstacle = Obstacle()
                    obstacles.append(obstacle)
            if event.key == pygame.K_d:
                debug = not debug

            if event.key == pygame.K_r:
                if states.getActualState() == "DRAWING_ROBOT":
                    print "Finish drawing the robot"
                    states.setActualState(None)
                else:
                    print "Started drawing the robot"
                    states.setActualState("DRAWING_ROBOT")
                    #create empty polygon and append to obstacles list
                    robot = Robot()

            if event.key == pygame.K_t:
                if states.getActualState() != "SELECT_TARGET":
                    print "Select the target point"
                    states.setActualState("SELECT_TARGET")
                    target = Target()
            if event.key == pygame.K_SPACE:
                if (target != None and robot != None):
                    states.setActualState("COMPUTING")


    #Main Logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if states.getActualState() == "COMPUTING" and robot != None:
        #(V, E) = visibility_graph(obstacles, robot.vertices[0], target.vertices[0])
        start_time = time.time()
        minus_robot = Robot()
        minus_vertices = []
        ref_point = robot.getRefPoint()
        for v in robot.vertices:
            minus_v = [None, None]
            minus_v[0] = 2*ref_point[0] - v[0]
            minus_v[1] = 2*ref_point[1] - v[1]
            minus_vertices.append((minus_v[0], minus_v[1]))
        minus_robot.vertices = minus_vertices
        c_obstacles = []
        for obstacle in obstacles:
            c_obs = C_Obstacle()
            c_obs.setVertices(GeoUtils.convex_hull(GeoUtils.mink_sum(minus_robot, obstacle)))
            c_obstacles.append(c_obs)
        Graph = visibility_graph(c_obstacles, robot.getRefPoint(), target.vertices[0])
        path = Graph.DijkstraShortestPath(robot.getRefPoint(), target.vertices[0])
        elapsed_time = time.time() - start_time
        #this is for representation, not measured (time)
        pathEdges = []
        for i in range(len(path)-2):
            pathEdges.append((path[i], path[i+1]))
        pathEdges.append((path[len(path)-2], path[len(path)-1]))
        V = Graph.V
        E = Graph.E

        states.setActualState(None)

    #Renders
    screen.fill(background_colour)
    if debug:
        for c_obstacle in c_obstacles:
            c_obstacle.draw(screen)

    for obstacle in obstacles:
        obstacle.draw(screen)
    #draw the robot
    if (robot != None):
        robot.draw(screen)
    #draw the target
    if (target != None):
        target.draw(screen)
    #draw visibility graph
    if debug:
        if (E != None):
            for e in E:
                pygame.draw.line(screen, (0,255,0), e[0], e[1])
        if (len(pathEdges) > 0):
            for e in pathEdges:
                pygame.draw.line(screen, (255,0,255), e[0], e[1], 3)
    else:
        if (len(pathEdges) > 0):
            for e in pathEdges:
                pygame.draw.line(screen, (255,0,255), e[0], e[1], 3)
    #draw text
    label = font.render("Number of obstacles: "+str(len(obstacles)), 1, (0,0,0))
    screen.blit(label, (0, 0))
    label = font.render("Time to compute: "+str(elapsed_time), 1, (0,0,0))
    screen.blit(label, (280, 0))
    label = font.render("Actual State: "+states.getActualState(), 1, (0,0,0))
    screen.blit(label, (0, 12))
    label = font.render("DEBUG: "+str(debug), 1, (0,0,0))
    screen.blit(label, (280, 12))
    label = font.render("R - draw Robot / O - draw Obstacle / T - place Target / SPACE - Compute", 1, (0,0,0))
    screen.blit(label, (0, 24))
    #swap
    pygame.display.flip()