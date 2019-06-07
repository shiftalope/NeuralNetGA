import sys
sys.path.insert(0, '../Utils/')
import Shapes
import pygame

class QuadTree():
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary
        self.capacity = capacity
        self.divided = False
        
        self.points = []
        
    def divide(self):
        self.divided = True
        cx = self.boundary.center.x; cy = self.boundary.center.y
        w = self.boundary.w; h=self.boundary.h

        ul_rect = Shapes.Rect(Shapes.Point(cx - w/4., cy - h/4.), w/2., h/2.)
        self.ul = QuadTree(ul_rect, self.capacity)
        ur_rect = Shapes.Rect(Shapes.Point(cx + w/4., cy - h/4.), w/2., h/2.)
        self.ur = QuadTree(ur_rect, self.capacity)
        ll_rect = Shapes.Rect(Shapes.Point(cx - w/4., cy + h/4.), w/2., h/2.)
        self.ll = QuadTree(ll_rect, self.capacity)
        lr_rect = Shapes.Rect(Shapes.Point(cx + w/4., cy + h/4.), w/2., h/2.)
        self.lr = QuadTree(lr_rect, self.capacity)
    
        for point in self.points:
            self.ul.insert(point)
            self.ur.insert(point)
            self.ll.insert(point)
            self.lr.insert(point)

        self.points = []
        
    def insert(self, point):
        if not self.boundary.pointInside(point): return
        
        if(len(self.points) < self.capacity and self.divided == False):
            self.points += [point]
        else:
            if(self.divided == False): self.divide()

            self.ul.insert(point)
            self.ur.insert(point)
            self.ll.insert(point)
            self.lr.insert(point)

    def getLocal(self, center, radius, lpoints = []):
        to_add = []
        if not self.boundary.circleInside(center, radius): return to_add
        else:
            for lpoint in self.points:
                if lpoint.dist(center) < radius: to_add += [lpoint]
            
            if self.divided:
                
                to_add += self.ul.getLocal(center, radius, lpoints)
                to_add += self.ur.getLocal(center, radius, lpoints)
                to_add += self.ll.getLocal(center, radius, lpoints)
                to_add += self.lr.getLocal(center, radius, lpoints)
    
        return to_add
        
    def show(self, canvas):
        self.boundary.show(canvas, stroke=1)
        if(self.divided):
            self.ul.show(canvas)
            self.ur.show(canvas)
            self.ll.show(canvas)
            self.lr.show(canvas)

if __name__ == '__main__':
    p1 = Shapes.Point(400,400)
    r1 = Shapes.Rect(p1, 800, 800)
    q1 = QuadTree(r1, 4)
    rad = 50
    
    pygame.init()
    gameDisplay = pygame.display.set_mode((800,800))
    gameDisplay.fill((255,255,255))
    clock = pygame.time.Clock()

    points = [Shapes.Point(rx=800, ry=800, rvx=10, rvy=10) for i in range(200)]
    running = True
    while running:
        pygame.display.update()
        gameDisplay.fill((255,255,255))
    
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_k]): running = False
        
#        pos = pygame.mouse.get_pos()
#        mpoint = Shapes.Point(pos[0], pos[1])
#        pygame.draw.circle(gameDisplay, (255,0,0), (int(mpoint.x), int(mpoint.y)), int(rad), 1)
#        pygame.draw.circle(gameDisplay, (255,0,0), (int(mpoint.x+800), int(mpoint.y)),int(rad), 1)
#        pygame.draw.circle(gameDisplay, (255,0,0), (int(mpoint.x-800), int(mpoint.y)),int(rad), 1)
#        pygame.draw.circle(gameDisplay, (255,0,0), (int(mpoint.x), int(mpoint.y+800)),int(rad), 1)
#        pygame.draw.circle(gameDisplay, (255,0,0), (int(mpoint.x), int(mpoint.y-800)),int(rad), 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False;

        q1 = QuadTree(r1, 4)
        
        for point in points:
            point.updatePos()
        
        for point in points:
            q1.insert(point)
            if point == points[0]: point.show(gameDisplay, color=(0,0,255), radius = 4)
            else: point.show(gameDisplay)

        for point in points:
            point.local_points = []
            point.local_points += q1.getLocal(Shapes.Point(point.x, point.y), rad, point.local_points)
            point.local_points += q1.getLocal(Shapes.Point(point.x-800, point.y), rad, point.local_points)
            point.local_points += q1.getLocal(Shapes.Point(point.x+800, point.y), rad, point.local_points)
            point.local_points += q1.getLocal(Shapes.Point(point.x, point.y-800), rad, point.local_points)
            point.local_points += q1.getLocal(Shapes.Point(point.x, point.y+800), rad, point.local_points)

            for otherp in point.local_points:
                p1_x = otherp.x; p1_y=otherp.y
                if (p1_x - point.x) > 400: p1_x -= 800
                if (p1_x - point.x) < -400: p1_x += 800
                if (p1_y - point.y) > 400: p1_y -= 800
                if (p1_y - point.y) < -400: p1_y += 800
                if point == points[0]:
                    pygame.draw.line(gameDisplay, (0,255,0), (point.x, point.y), (p1_x, p1_y), 4)
                else:
                    pygame.draw.line(gameDisplay, (255,0,0), (point.x, point.y), (p1_x, p1_y))
        
        #q1.show(gameDisplay)

        clock.tick(60)
