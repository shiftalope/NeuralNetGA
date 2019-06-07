import pygame
import random
import numpy as np

MAX_ACCEL = .5
MAX_VEL = 10.

class Point():
    def __init__(self, x = 0, y = 0, vx=0, vy=0, rx = None, ry = None, rvx=None, rvy=None):
        self.x = x; self.y = y;
        self.vx = vx; self.vy=vy
        self.ax = 0; self.ay=0
    
        #if rx != None: self.x = np.random.normal(400, 100)
        #if ry != None: self.y = np.random.normal(400, 100)
        if rx != None: self.x = np.random.uniform(800)
        if ry != None: self.y = np.random.uniform(800)
        if rvx != None: self.vx = random.uniform(-1*rvx, rvx)
        if rvy != None: self.vy = random.uniform(-1*rvx, rvy)

    def show(self, canvas, color=(0,0,0), radius=2):
        pygame.draw.circle(canvas, color, (int(self.x), int(self.y)), radius)

    def dist(self, point2):
        diff_x = abs(self.x-point2.x)
        diff_y = abs(self.y-point2.y)
        if diff_x > 400: diff_x = 800 - diff_x
        if diff_y > 400: diff_y = 800 - diff_y
        
        return np.sqrt(diff_x**2 + diff_y**2)

    def updatePos(self):
        self.x+=self.vx; self.y+=self.vy

        if self.x > 800: self.x -= 800
        if self.y > 800: self.y -= 800
        if self.x < 0: self.x += 800
        if self.y < 0: self.y += 800
    
    def updateVel(self):
        if self.ax != 0 and self.ay !=0:
            self.ax = MAX_ACCEL * self.ax / np.sqrt(self.ax**2 + self.ay**2)
            self.ay = MAX_ACCEL * self.ay / np.sqrt(self.ax**2 + self.ay**2)
        
        self.vx += self.ax; self.vy += self.ay
        
        #tmp_vx = self.vx / np.sqrt(self.vx**2 + self.vy**2)
        #tmp_vy = self.vy / np.sqrt(self.vx**2 + self.vy**2)
        
        if self.vx > MAX_VEL/np.sqrt(2): self.vx = MAX_VEL/np.sqrt(2)
        if self.vy > MAX_VEL/np.sqrt(2): self.vy = MAX_VEL/np.sqrt(2)
        if self.vx < -1*MAX_VEL/np.sqrt(2): self.vx = -1*MAX_VEL/np.sqrt(2)
        if self.vy < -1*MAX_VEL/np.sqrt(2): self.vy = -1*MAX_VEL/np.sqrt(2)
        self.ax=0; self.ay=0
        
    def updateAccel(self, avec):
        self.ax += avec.x; self.ay += avec.y
        
#        if self.ax != 0 and self.ay != -0:
#            tmp_ax = MAX_ACCEL * self.ax
#            tmp_ay = MAX_ACCEL * self.ay
#    
#            self.ax=tmp_ax; self.ay=tmp_ay
    
    def avg_local_vel(self, scale=1):
        lvel_x = 0; lvel_y = 0;
        for lpoint in self.local_points:
            lvel_x += lpoint.vx/float(len(self.local_points))
            lvel_y += lpoint.vy/float(len(self.local_points))
    
        accel_x = 0; accel_y = 0;
        if len(self.local_points)-1 != 0:
            tmp_x = (lvel_x)/float(len(self.local_points)-1)
            tmp_y = (lvel_y)/float(len(self.local_points)-1)
        
            if tmp_x != 0 or tmp_y != 0:
                accel_x = tmp_x / np.sqrt(tmp_x**2 + tmp_y**2)
                accel_y = tmp_y / np.sqrt(tmp_x**2 + tmp_y**2)

        else:
            accel_x = 0
            accel_y = 0

        return Point(scale*accel_x, scale*accel_y)

    def avg_local_pos(self, scale=1):
        lpos_x = 0; lpos_y = 0;
        for lpoint in self.local_points:
            lpos_x += lpoint.x / float(len(self.local_points));
            lpos_y += lpoint.y / float(len(self.local_points))
        
        accel_x = 0; accel_y = 0;
        if len(self.local_points)-1 != 0:
            diff_x = lpos_x-self.x; diff_y = lpos_y-self.y
            if diff_x > 400: diff_x -= 800
            if diff_x < -400: diff_x += 800
            if diff_y > 400: diff_y -= 800
            if diff_y < -400: diff_y += 800
            
            tmp_x = (diff_x)/float(len(self.local_points)-1)
            tmp_y = (diff_y)/float(len(self.local_points)-1)

            if tmp_x != 0 or tmp_y != 0:
                accel_x = tmp_x / np.sqrt(tmp_x**2 + tmp_y**2)
                accel_y = tmp_y / np.sqrt(tmp_x**2 + tmp_y**2)
           
        else:
            accel_x = 0
            accel_y = 0

        return Point(scale*accel_x, scale*accel_y)

    def avoid(self, scale=1):
        if len(self.local_points) == 1: return Point(0,0)
        tmp_x = 0; tmp_y = 0
        for lpoint in self.local_points:
            diff_x = self.x - lpoint.x
            diff_y = self.y - lpoint.y
            
            if diff_x == 0 and diff_y == 0: continue
            if diff_x > 400: diff_x -= 800
            if diff_x < -400: diff_x += 800
            if diff_y > 400: diff_y -= 800
            if diff_y < -400: diff_y += 800
            
            tmp_x += diff_x / (diff_x**2 + diff_y**2)
            tmp_y += diff_y / (diff_x**2 + diff_y**2)

        tmp_x = tmp_x / len(self.local_points)
        tmp_y = tmp_y / len(self.local_points)

        accel_x = 0; accel_y = 0;
        if tmp_x != 0 or tmp_y != 0:
            accel_x = tmp_x / np.sqrt(tmp_x**2 + tmp_y**2)
            accel_y = tmp_y / np.sqrt(tmp_x**2 + tmp_y**2)

        return Point(scale*accel_x, scale*accel_y)




class Rect():
    def __init__(self, center = None, w=None, h=None):
        self.center = center; self.w = w; self.h = h

    def show(self, canvas, color=(0,0,0), stroke=2):
        rect = (self.center.x - self.w/2., self.center.y - self.h/2., self.w, self.h)
        pygame.draw.rect(canvas, color, rect, stroke)

    def pointInside(self, point):
        return (point.x < self.center.x+self.w/2. and
                point.x > self.center.x-self.w/2. and
                point.y > self.center.y-self.w/2. and
                point.y < self.center.y+self.w/2.)

    def circleInside(self, point, radius):
        inside = True
        if point.x + radius <= self.center.x - self.w/2. : inside = False
        if point.x - radius > self.center.x + self.w/2. : inside = False
        if point.y + radius <= self.center.y - self.h/2. : inside = False
        if point.y - radius > self.center.y + self.h/2. : inside = False

        return inside
