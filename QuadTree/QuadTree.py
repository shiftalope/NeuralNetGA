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
        
    def insert(self, point):
        if not self.boundary.pointInside(point): return
        
        if(len(self.points) < self.capacity):
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
        self.boundary.show(canvas)
        if(self.divided):
            self.ul.show(canvas)
            self.ur.show(canvas)
            self.ll.show(canvas)
            self.lr.show(canvas)
