import sys
import pygame
import numpy as np
import random
import multiprocessing as mp
import pickle
from functools import partial

sys.path.insert(0, 'NEATer/')
sys.path.insert(0, 'QuadTree/')
sys.path.insert(0, 'Utils/')
import Node
import QuadTree
import Shapes

def blah():
    print('blah')

class player():
    
    def __init__(self, canvas, x=None, y=None, vx=None, vy=None, ax=0, ay=0,
                 rpos = False, rvel = False, max_vel = 10,
                 mass = 10, color = (0,0,255), brain = None, radius = 50):
        #self.canvas = canvas;
        self.cw = canvas.get_width(); self.ch = canvas.get_height();
        self.x = x; self.y = y; self.vx = vx; self.vy = vy; self.ax = ax; self.ay = ay;
        self.mass = mass; self.alive=True; self.color = color
        self.max_vel = max_vel; self.rpos = rpos; self.rvel = rvel
        self.brain = brain; self.rad = radius

        if brain == None: self.brain = Node.Network(iNodes_n=6, oNodes_n=4)#, hNodes_n=4)
    
        self.reset()
    
    def show(self, canvas, color=None):
        if color == None: UseColor = self.color
        else: UseColor = color
        
        ulx = self.x-self.mass/2.; uly = self.y-self.mass/2.;
        llx = self.x+self.mass/2.; lly = self.y+self.mass/2.;
        
        pygame.draw.rect(canvas, UseColor, pygame.Rect(ulx, uly, self.mass, self.mass), 0)
    
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
        
        if self.x > self.cw: self.x -= self.cw
        if self.y > self.ch: self.y -= self.ch
        if self.x < 0: self.x += self.cw
        if self.y < 0: self.y += self.ch

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

def decision(player2, qTree):
    if not player2.alive: return (None, None, None, None)
#    print('Making Decision...')
    locals = qTree.getLocal(Shapes.Point(player2.x, player2.y), player2.rad)
    avg_x = 0; avg_y = 0
    avg_vx = 0; avg_vy = 0
    for local in locals:
        #pygame.draw.line(player2.canvas, (0,255,0), (player2.x, player2.y), (local.x, local.y), 4)
        avg_x += local.x; avg_y += local.y
        avg_vx += local.vx; avg_vy += local.vy

    if float(len(locals)) != 0:
        avg_x /= float(len(locals)); avg_y /= float(len(locals))
        avg_vx /= float(len(locals)); avg_vy /= float(len(locals))

#    print('Decision Made!')
    return (avg_x, avg_y, avg_vx, avg_vy)

nPlayers = 1000
width = 900; length = 900;
pygame.init()
gameDisplay = pygame.display.set_mode((width,length))
gameDisplay.fill((255,255,255))
clock = pygame.time.Clock()
rad = 100

players = [player(gameDisplay, radius = rad, rpos=True) for i in range(nPlayers)]
opponents = [player(gameDisplay, color=(255,0,0), rpos=True, rvel=True, max_vel=2) for i in range(100)]


p1 = Shapes.Point(width/2.,length/2.)
r1 = Shapes.Rect(p1, width, length)

running = True
gens = 0
while running:
    gens += 1
    start_zone = Shapes.Rect(p1, w=100, h=100)
    for opponent in opponents:
        pos_i = Shapes.Point(opponent.x, opponent.y)
        while(start_zone.pointInside(pos_i)):
            opponent.x = random.uniform(0, width)
            opponent.y = random.uniform(0, length)
            pos_i = Shapes.Point(opponent.x, opponent.y)

    running1 = True
    pygame.init()
    gameDisplay = pygame.display.set_mode((width,length))
    gameDisplay.fill((255,255,255))
    clock = pygame.time.Clock()
    
    iters = 0
    while any([player1.alive for player1 in players]) and running1:
        #print(iters)
        iters+=1
        pygame.display.update()
        gameDisplay.fill((255,255,255))
        
        q1 = QuadTree.QuadTree(r1, 4, keys=['x','y'])
        for player1 in players:
            if player1.alive:
                player1.show(gameDisplay)
                if player1.color == (0,255,0): pygame.draw.circle(gameDisplay, (0,255,0), (int(player1.x), int(player1.y)), rad, 1)
                q1.insert(player1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False; running1 = False
            
            keys = pygame.key.get_pressed()
            if(keys[pygame.K_k]): running1 = False
        
        q2 = QuadTree.QuadTree(r1, 4, keys=['x','y'])
        for opponent in opponents:
            q2.insert(opponent)
            opponent.update()
            opponent.show(gameDisplay)
    
#        decision2 = partial(decision, qTree=q1) # prod_x has only one argument x (y is fixed to 10)
#        pool = mp.Pool(mp.cpu_count())
#        avgs = pool.map(decision2, players)
#        pool.close()

        for index in range(len(players)):
            player1 = players[index]
#            player1.avg_x = avgs[index][0]
#            player1.avg_y = avgs[index][1]
#            player1.avg_vx = avgs[index][2]
#            player1.avg_vy = avgs[index][3]
            player1.avg_x = 0
            player1.avg_y = 0
            player1.avg_vx = 0
            player1.avg_vy = 0

            if not player1.alive: continue
            player1.score += 1
#            locals = q1.getLocal(Shapes.Point(player1.x, player1.y), rad)
#            avg_x = 0; avg_y = 0
#            avg_vx = 0; avg_vy = 0
#            for local in locals:
#                pygame.draw.line(gameDisplay, (0,255,0), (player1.x, player1.y), (local.x, local.y), 4)
#                avg_x += local.x; avg_y += local.y
#                avg_vx += local.vx; avg_vy += local.vy

#            if float(len(locals)) != 0:
#                avg_x /= float(len(locals)); avg_y /= float(len(locals))
#                avg_vx /= float(len(locals)); avg_vy /= float(len(locals))

            foes = q2.getLocal(Shapes.Point(player1.x, player1.y), rad)
            foe_x = 0; foe_y = 0;
            for foe in foes:
                diff_x = (player1.x - foe.x); diff_y = (player1.y - foe.y)
                dist = np.sqrt(diff_x**2+diff_y**2)
                
                foe_x += diff_x/dist; foe_y += diff_y/dist
                if (abs(player1.x - foe.x) < (player1.mass + foe.mass)/2. and
                    abs(player1.y - foe.y) < (player1.mass + foe.mass)/2.): player1.alive = False
            
            if len(foes) != 0: foe_x = foe_x/float(len(foes)); foe_y = foe_y/float(len(foes))
                                                               
            player.state = [
                            #player1.x/float(width),
                            #player1.y/float(length),
#                            player1.vx/np.sqrt(player1.vx**2 + player1.vy**2 + 0.1),
#                            player1.vy/np.sqrt(player1.vx**2 + player1.vy**2 + 0.1),
                            player1.avg_x/float(width),
                            player1.avg_y/float(length),
                            player1.avg_vx/np.sqrt(player1.avg_vx**2 + player1.avg_vy**2 + 0.1),
                            player1.avg_vx/np.sqrt(player1.avg_vx**2 + player1.avg_vy**2 + 0.1),
                            foe_x/float(width),
                            foe_y/float(length),
#                            1
                            ]

            
            for sense in range(len(player.state)):
                player1.brain.iNodes[sense].val = player1.state[sense]

            player1.brain.updateNet()
            UDRL = [node.val for node in player1.brain.oNodes]
            if UDRL[0] == max(UDRL): player1.addForce((0,-1))
            elif UDRL[1] == max(UDRL): player1.addForce((0,1))
            elif UDRL[2] == max(UDRL): player1.addForce((-1,0))
            elif UDRL[3] == max(UDRL): player1.addForce((1,0))

            
            player1.update()
            #if (player1.x < 0 or player1.x > width or player1.y < 0 or player1.y > length): player1.alive=False

                
        q1.show(gameDisplay)
        clock.tick(60)
        #if iters > 600: running1 = False

    nBest = -10
    scores = [player1.score for player1 in players]
    best_i = sorted(range(len(scores)), key=lambda i: scores[i])[nBest:]
    for opponent in opponents:
        opponent.reset()

    for player1 in players:
        if player1 == players[0]: player1.brain.graph()
        player1.color = (0,255,0)
        player1.reset()

    if np.max(scores) == 1: print('EXTINCTION EVENT!'); continue
    print('MAX:', np.max(scores), 'MEAN:', np.mean(scores))


    players = [players[i] for i in best_i]
    copies = int(nPlayers/len(players))-1
    for i in range(10):
        for copy in range(copies):
            new_brain = players[i].brain.get_mutation(iters=gens, lr=2)
            new_player = player(gameDisplay, brain=new_brain, rpos=players[0].rpos)
            players += [new_player]
