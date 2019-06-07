import sys
sys.path.insert(0, 'Utils/')
sys.path.insert(0, 'QuadTree/')
sys.path.insert(0, 'NEATer/')
import Node
import pygame
import random


class new_player():
    
    def __init__(self, canvas,
                 nInputs, nOutputs, nHidden=0,
                 prand=False, vrand=False,
                 alive=True, score=0 ,
                 state = [], brain = None):
        
        self.nInputs = nInputs; self.nOutputs = nOutputs; self.nHidden = nHidden;
        
        hig = canvas.get_height()
        wid = canvas.get_width()
        self.xpos = wid/2 + random.uniform(-1*wid/2, wid/2) * int(prand)
        self.ypos = hig/2 + random.uniform(-1*hig/2, hig/2) * int(prand)
        self.xvel = random.uniform(-1, 1) * int(vrand)
        self.yvel = random.uniform(-1, 1) * int(vrand)

        self.alive=alive; self.score=0
        self.state = state;
        if brain != None: self.brain=brain
        else: self.brain=Node.Network(self.nInputs, self.nOutputs, self.nHidden)

    def reset(self, canvas, rand=False):
        hig = canvas.get_height()
        wid = canvas.get_width()
        self.xpos = wid/2 + random.uniform(-1*wid/2, wid/2) * int(rand)
        self.ypos = hig/2 + random.uniform(-1*hig/2, hig/2) * int(rand)
        self.xvel=0
        self.yvel=0
        
        self.alive=True
        self.score=0

    def show(self, canvas, color=(0,0,0), radius=2):
        pygame.draw.circle(canvas, color, (int(self.xpos), int(self.ypos)), radius)

if __name__ == '__main__':

    pygame.init()
    gameDisplay = pygame.display.set_mode((1000,800))
    gameDisplay.fill((255,255,255))
    clock = pygame.time.Clock()
    
    player = new_player(gameDisplay, 4,2)

    running = True
    while running:
        pygame.display.update()
        gameDisplay.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False;
        
        player.show(gameDisplay)
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_k]):
            player.reset(gameDisplay, rand=True)
            print(player.xpos, player.ypos)

        clock.tick(60)
