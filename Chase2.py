import sys
import pygame
import numpy as np
import random

sys.path.insert(0, 'NEATer/')
sys.path.insert(0, 'QuadTree/')
sys.path.insert(0, 'Utils/')
import Node
import QuadTree
import Shapes

class player():
    
    def __init__(self, canvas, x=None, y=None, vx=None, vy=None, ax=0, ay=0,
                 rpos = False, rvel = False, max_vel = 10,
                 mass = 10, color = (0,0,255)):
        self.canvas = canvas; self.cw = self.canvas.get_width(); self.ch = self.canvas.get_height();
        self.x = x; self.y = y; self.vx = vx; self.vy = vy; self.ax = ax; self.ay = ay;
        self.mass = mass; self.alive=True; self.color = color
        self.max_vel = max_vel; self.rpos = rpos; self.rvel = rvel

        self.brain = Node.Network(iNodes_n=8, oNodes_n=4, hNodes_n=4)
    
        self.reset()
    
    def show(self, color=None):
        if color == None: UseColor = self.color
        else: UseColor = color
        
        ulx = self.x-self.mass/2.; uly = self.y-self.mass/2.;
        llx = self.x+self.mass/2.; lly = self.y+self.mass/2.;
        
        pygame.draw.rect(self.canvas, UseColor, pygame.Rect(ulx, uly, self.mass, self.mass), 0)
    
    def addForce(self, force):
        self.ax += force[0]; self.ay += force[1]

    def update(self, scale=1):
        self.vx += self.ax*scale
        self.vy += self.ay*scale
        
        if self.vx > self.max_vel / np.sqrt(2): self.vx = self.max_vel / np.sqrt(2)
        if self.vx < -1*self.max_vel / np.sqrt(2): self.vx = -1 * self.max_vel / np.sqrt(2)
        if self.vy > self.max_vel / np.sqrt(2): self.vy = self.max_vel / np.sqrt(2)
        if self.vy < -1*self.max_vel / np.sqrt(2): self.vy = -1 * self.max_vel / np.sqrt(2)

        self.x += self.vx*scale
        self.y += self.vy*scale
        
#        if self.x > self.canvas.get_width(): self.x -= self.canvas.get_width()
#        if self.y > self.canvas.get_height(): self.y -= self.canvas.get_height()
#        if self.x < 0: self.x += self.canvas.get_width()
#        if self.y < 0: self.y += self.canvas.get_height()

        self.ax = 0; self.ay = 0
    
    def mutate_brain(self):
        self.brain = self.brain.get_mutation()

    def reset(self):
        
        if self.rpos:
            self.x = random.uniform(0, self.cw)
            self.y = random.uniform(0, self.ch)
        else:
            self.x = self.cw/2.
            self.y = self.ch/2.
        
            
        self.vx = random.uniform(-1*self.max_vel / np.sqrt(2), 1*self.max_vel / np.sqrt(2))
        self.vy = random.uniform(-1*self.max_vel / np.sqrt(2), 1*self.max_vel / np.sqrt(2))
        
        self.alive=True
        self.score=0

nPlayers = 100
width = 900; length = 900;
pygame.init()
gameDisplay = pygame.display.set_mode((width,length))
gameDisplay.fill((255,255,255))
clock = pygame.time.Clock()

players = [player(gameDisplay) for i in range(nPlayers)]
opponents = [player(gameDisplay, color=(255,0,0), rpos=True) for i in range(nPlayers)]

p1 = Shapes.Point(width/2.,length/2.)
r1 = Shapes.Rect(p1, width, length)
rad = 50

running = True
while running:

    running1 = True
    pygame.init()
    gameDisplay = pygame.display.set_mode((width,length))
    gameDisplay.fill((255,255,255))
    clock = pygame.time.Clock()
    
    iters = 0
    while any([player.alive for player in players]) and running1:
        iters+=1
        pygame.display.update()
        gameDisplay.fill((255,255,255))
        
        q1 = QuadTree.QuadTree(r1, 4, keys=['x','y'])
        for player in players:
            if player.alive:
                player.show()
                q1.insert(player)
            if player == players[0]: player.show(color=(0,255,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False; running1 = False
            
            keys = pygame.key.get_pressed()
            if(keys[pygame.K_k]): running1 = False
        
        q2 = QuadTree.QuadTree(r1, 4, keys=['x','y'])
        for opponent in opponents:
            q2.insert(opponent)
            opponent.show()

        for player in players:
            if not player.alive: continue
            player.score += 1
            locals = q1.getLocal(Shapes.Point(player.x, player.y), rad)
            avg_x = 0; avg_y = 0
            avg_vx = 0; avg_vy = 0
            for local in locals:
                pygame.draw.line(gameDisplay, (0,255,0), (player.x, player.y), (local.x, local.y), 4)
                avg_x += local.x; avg_y += local.y
                avg_vx += local.vx; avg_vy += local.vy

            if float(len(locals)) != 0:
                avg_x /= float(len(locals)); avg_y /= float(len(locals))
                avg_vx /= float(len(locals)); avg_vy /= float(len(locals))
            
            foes = q2.getLocal(Shapes.Point(player.x, player.y), rad)
            for foe in foes:
                if (abs(player.x - foe.x) < (player.mass + foe.mass)/2. and
                    abs(player.y - foe.y) < (player.mass + foe.mass)/2.): player.alive = False
            
            player.state = [player.x/float(width),
                            player.y/float(length),
                            player.vx/np.sqrt(player.vx**2 + player.vy**2 + 0.1),
                            player.vy/np.sqrt(player.vx**2 + player.vy**2 + 0.1),
                            avg_x/float(width),
                            avg_y/float(length),
                            avg_vx/np.sqrt(avg_vx**2 + avg_vy**2 + 0.1),
                            avg_vx/np.sqrt(avg_vx**2 + avg_vy**2 + 0.1),]

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

                
        q1.show(gameDisplay)
        clock.tick(60)
        if iters > 200: running1 = False

    scores = [player.score for player in players]
    print(max(scores))
    for player in players:
        player.reset()
        player.mutate_brain()
