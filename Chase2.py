import pygame
import numpy as np

class player():
    
    def __init__(self, canvas, x=None, y=None, vx=0, vy=0, ax=0, ay=0, mass=10):
        self.x = x; self.y = y;
        self.vx = vx; self.vy = vy;
        self.ax = ax; self.ay = ay;
        self.mass = mass;

        if self.x == None: self.x = canvas.get_width()/2
        if self.y == None: self.y = canvas.get_height()/2



    def show(self, canvas, color=(255,0,0)):
        ulx = self.x-self.mass/2.; uly = self.y-self.mass/2.;
        llx = self.x+self.mass/2.; lly = self.y+self.mass/2.;
        
        pygame.draw.rect(canvas, color, pygame.Rect(ulx, uly, self.mass, self.mass), 0)
    
    def addForce(self, force):
        self.ax += force[0]; self.ay += force[1]

    def update(self, scale):
        self.vx += self.ax*scale
        self.vy += self.ay*scale

        self.x += self.vx*scale
        self.y += self.vy*scale

        self.ax = 0; self.ay = 0

width = 800; length = 800;
pygame.init()
gameDisplay = pygame.display.set_mode((width,length))
gameDisplay.fill((255,255,255))
clock = pygame.time.Clock()

player = player(gameDisplay, y=200, vx=-10)

running = True
while running:
    pygame.display.update()
    gameDisplay.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False;
    
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_k]): running = False

    mini_steps = 100
    for i in range(mini_steps):
        R = np.sqrt((400-player.x)**2 + (400-player.y)**2)
        accel = ((player.vx)**2 + (player.vy)**2) / (R)
        dir = np.arctan(player.x/player.y)
        accel = (accel*(400-player.x)/R, accel*(400-player.y)/R)
        player.addForce(accel)

        player.update(1/float(mini_steps))

    player.show(gameDisplay)

    pygame.draw.circle(gameDisplay, (255,0,0), (400,400), 200, 1)

    clock.tick(60)
