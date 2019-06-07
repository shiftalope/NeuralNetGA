import sys
import pygame
import numpy as np
import random

sys.path.insert(0, 'NEATer/')
import Node

class player():
    
    def __init__(self, canvas, x=None, y=None, vx=0, vy=0, ax=0, ay=0, mass=10):
        self.x = x; self.y = y;
        self.vx = vx; self.vy = vy;
        self.ax = ax; self.ay = ay;
        self.mass = mass; self.alive=True

        if self.x == None: self.x = canvas.get_width()/2
        if self.y == None: self.y = canvas.get_height()/2

        self.brain = Node.Network(iNodes_n=4, oNodes_n=4, hNodes_n=4)
    
    def show(self, canvas, color=(255,0,0)):
        ulx = self.x-self.mass/2.; uly = self.y-self.mass/2.;
        llx = self.x+self.mass/2.; lly = self.y+self.mass/2.;
        
        pygame.draw.rect(canvas, color, pygame.Rect(ulx, uly, self.mass, self.mass), 0)
    
    def addForce(self, force):
        self.ax += force[0]; self.ay += force[1]

    def update(self, scale=1):
        self.vx += self.ax*scale
        self.vy += self.ay*scale

        self.x += self.vx*scale
        self.y += self.vy*scale

        self.ax = 0; self.ay = 0
    
    def mutate_brain(self):
        self.brain = self.brain.get_mutation()

    def reset(self, canvas):
        self.x=canvas.get_width()/2.
        self.y=canvas.get_height()/2.
        self.vx=random.uniform(-1,1)
        self.vy=random.uniform(-1,1)
        
        self.alive=True
        self.score=0

nPlayers = 200
width = 800; length = 800;
pygame.init()
gameDisplay = pygame.display.set_mode((width,length))
gameDisplay.fill((255,255,255))
clock = pygame.time.Clock()

players = [player(gameDisplay) for i in range(nPlayers)]

running = True
while running:

    running1 = True
    pygame.init()
    gameDisplay = pygame.display.set_mode((width,length))
    gameDisplay.fill((255,255,255))
    clock = pygame.time.Clock()
    
    while any([player.alive for player in players]) and running1:
        pygame.display.update()
        gameDisplay.fill((255,255,255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False; running1 = False
            
            keys = pygame.key.get_pressed()
            if(keys[pygame.K_k]): running1 = False

        for player in players:

            if not player.alive: continue
            player.state = [player.x/float(width),
                            player.y/float(length),
                            player.vx/np.sqrt(player.vx**2 + player.vy**2 + 0.1),
                            player.vy/np.sqrt(player.vx**2 + player.vy**2 + 0.1)]

            for sense in range(len(player.state)):
                player.brain.iNodes[sense].val = player.state[sense]

            player.brain.updateNet()
            UDRL = [node.val for node in player.brain.oNodes]
            if UDRL[0] == max(UDRL): player.addForce((0,-1))
            elif UDRL[1] == max(UDRL): player.addForce((0,1))
            elif UDRL[2] == max(UDRL): player.addForce((-1,0))
            elif UDRL[3] == max(UDRL): player.addForce((1,0))

            player.update()
            if (player.x < 0 or player.x > width or player.y < 0 or player.y > length): player.alive=False
            player.show(gameDisplay)

        clock.tick(60)

    for player in players:
        player.reset(gameDisplay)
        player.mutate_brain()
