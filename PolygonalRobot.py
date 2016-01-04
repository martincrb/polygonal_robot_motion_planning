import pygame
from Elements import *
from State import *

#Start main window
dimensions = (800, 600)
screen = pygame.display.set_mode(dimensions)
pygame.display.set_caption('Polygonal Robot: motion planning')
background_colour = (255,255,255)
clock = pygame.time.Clock()
running = True
#fonts
pygame.font.init()
font = pygame.font.SysFont("monospace", 15)



#logic elements
obstacles = []
robot = None
target = None

#define global state of application
states = State()

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


    #Main Logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Renders
    screen.fill(background_colour)
    for obstacle in obstacles:
        obstacle.draw(screen)
    #draw the robot
    if (robot != None):
        robot.draw(screen)
    #draw the target
    if (target != None):
        target.draw(screen);

    #draw text
    label = font.render("Number of obstacles: "+str(len(obstacles)), 1, (0,0,0))
    screen.blit(label, (0, 0))
    label = font.render("Actual State: "+states.getActualState(), 1, (0,0,0))
    screen.blit(label, (0, 10))

    #swap
    pygame.display.flip()