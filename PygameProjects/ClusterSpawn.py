import pygame
import sys
from random import *

# Don't ask me what this is, I just thought it was neat.
# I suppose I had some idea of playing around with vertices and edges.
# Could be interesting to do some more "math" programming since it produces interesting results.
# For now it's just vertices connected by edges according to their index in the list.
# They move around in a seemingly random manner, looks kinda neat when you have many of them.

class Vertex:
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.r = randint(0, 255)
        self.g = randint(0, 255)
        self.b = randint(0, 255)
        
    def draw(self):
        pygame.draw.circle(screen, (self.r, self.g, self.b), (self.x, self.y), 10)
        
    def findNeighbor(self, nodes: list):
        for i in range(len(nodes) - 1):
            pygame.draw.line(screen, (255,255,255), (nodes[i].x, nodes[i].y), (nodes[i+1].x, nodes[i+1].y))
        
    def move(self):
        if not hasattr(self, 'target_pos'):
            self.target_pos = self.makeNewPos()

        currentPos = (self.x, self.y)
        targetPos = self.target_pos

        if abs(targetPos[0] - self.x) > 0.1:
            self.x += 0.1 if targetPos[0] > self.x else - 0.1
        if abs(targetPos[1] - self.y) > 0.1:
            self.y += 0.1 if targetPos[1] > self.y else - 0.1

        if abs(targetPos[0] - self.x) <= 0.1 and abs(targetPos[1] - self.y) <= 0.1:
            self.target_pos = self.makeNewPos()

    def makeNewPos(self):
        return (randint(0, 800), randint(0, 600))
        
        



pygame.init()

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cluster Spawn")
nodesOnScreen = []


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if len(nodesOnScreen) < 15:
        node = Vertex(randint(0, WIDTH), randint(0, HEIGHT))
        nodesOnScreen.append(node)
                  
    screen.fill((0, 0, 0))
    
    
    for n in nodesOnScreen:
        n.draw()
        n.findNeighbor(nodesOnScreen)
        n.move()
    
    pygame.display.flip()

pygame.quit()
sys.exit()
