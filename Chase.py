import sys
sys.path.insert(0, 'Utils/')
sys.path.insert(0, 'QuadTree/')
from QuadTree import QuadTree
from Shapes import *
import pygame

width = 800; length = 800; rad = 50
v_scale = 1.5; a_scale = 2.5; p_scale = 4;
center = Point(width/2,length/2)
main_rect = Rect(center, width, length)

pygame.init()
gameDisplay = pygame.display.set_mode((width,length))
gameDisplay.fill((255,255,255))
clock = pygame.time.Clock()

players = [Point(rx=width, ry=length, rvx=10, rvy=10) for i in range(200)]
running = True
qTree = QuadTree(main_rect, 4)
for player in players:
    qTree.insert(player)

while running:
    pygame.display.update()
    gameDisplay.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False;
    
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_k]): running = False

    if(keys[pygame.K_q]): rad+=1; print('rad:', rad)
    if(keys[pygame.K_a]): rad-=1; print('rad:', rad)

    if(keys[pygame.K_w]): a_scale+=.1; print('a_scale:', a_scale)
    if(keys[pygame.K_s]): a_scale-=.1; print('a_scale:', a_scale)
    if(keys[pygame.K_e]): v_scale+=.1; print('v_scale:', v_scale)
    if(keys[pygame.K_d]): v_scale-=.1; print('v_scale:', v_scale)
    if(keys[pygame.K_r]): p_scale+=.1; print('p_scale:', p_scale)
    if(keys[pygame.K_f]): p_scale-=.1; print('p_scale:', p_scale)
    
    for player in players:
        player.local_points = []
        player.local_points += qTree.getLocal(player, rad, player.local_points)
        player.local_points += qTree.getLocal(Point(player.x-800, player.y), rad, player.local_points)
        player.local_points += qTree.getLocal(Point(player.x+800, player.y), rad, player.local_points)
        player.local_points += qTree.getLocal(Point(player.x, player.y-800), rad, player.local_points)
        player.local_points += qTree.getLocal(Point(player.x, player.y+800), rad, player.local_points)

        player.updateAccel(player.avg_local_vel(v_scale))
        player.updateAccel(player.avoid(a_scale))
        player.updateAccel(player.avg_local_pos(p_scale))

    qTree = QuadTree(main_rect, 4)
    for player in players:
        player.updateVel()
        player.updatePos()
        player.show(gameDisplay, radius=4)
        qTree.insert(player)

    for player in players:
        for otherp in player.local_points:
            p1_x = otherp.x; p1_y=otherp.y
            if (p1_x - player.x) > 400: p1_x -= 800
            if (p1_x - player.x) < -400: p1_x += 800
            if (p1_y - player.y) > 400: p1_y -= 800
            if (p1_y - player.y) < -400: p1_y += 800
            pygame.draw.line(gameDisplay, (255,0,0), (player.x, player.y), (p1_x, p1_y))

    qTree.show(gameDisplay)
    clock.tick(60)
