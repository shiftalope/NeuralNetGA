import numpy as np
import random as rand

#2 Dimensional Vector Class
class Vector2D():
    
    #Initializer, supports any combination of inputs and  fills in the rest if possible.
    def __init__(self, x=None, y=None, mag=None, dir=None):
        self.x=x; self.y=y; self.mag=mag; self.dir=dir
        
        #Set from X and Y only
        if x!=None and y!= None and mag==None and dir==None:
            self.x = float(x); self.y = float(y);
            self.SetMagDir()
            return
        
        #Set from Mag and Dir only
        elif x==None and y== None and mag!=None and dir!=None:
            self.mag = float(mag); self.dir = float(dir);
            self.x = mag*np.cos(dir); self.y = mag*np.sin(dir);
            return
        
        #Set everything to 0
        elif x==None and y== None and mag==None and dir==None:
            self.x = 0; self.y=0; self.mag=0; self.dir=0;
            return
        
        #If Dir and (X or Y) given, cannot compute.
        #If more than two inputs given, sets inputs
        #But doesn't check to see if they are consistent
        print('WARNING: Some inputs may not be set, or may be inconsistent with others')
    
    
    #Set Mag and Dir from X and Y
    #Dir between 0 and 2PI
    def SetMagDir(self):
        self.mag = np.sqrt(self.x**2 + self.y**2)
        
        #Checks if on y-axis, in the 2nd or 3rd quadrant, or negative and corrects
        if self.x != 0:
            self.dir = np.arctan(self.y/self.x) + np.pi * int(self.x < 0)
        else: self.dir = np.pi/2 + np.pi * int(self.y < 0)
        
        if self.dir < 0: self.dir += 2*np.pi

    #Vector Addition
    def __add__(self, V2):
        if type(V2) in [int, float]:
            return Vector2D(x = (self.x + V2),
                            y = (self.y + V2))
        if type(V2) in [Vector2D]:
            return Vector2D(x = (self.x + V2.x),
                            y = (self.y + V2.y))
    
    #Vector Subtraction
    def __sub__(self, V2):
        if type(V2) in [int, float]:
            return Vector2D(x = (self.x - V2),
                            y = (self.y - V2))
        if type(V2) in [Vector2D]:
            return Vector2D(x = (self.x - V2.x),
                            y = (self.y - V2.y))

    def __rsub__(self, V2):
        if type(V2) in [int, float]:
            return Vector2D(x = (V2 - self.x),
                            y = (V2 - self.y))
        if type(V2) in [Vector2D]:
             return Vector2D(x = (V2.x - self.x),
                             y = (V2.y - self.y))

    #Scalar and Dot Product Multiplication
    def __mul__(self, other):
        if type(other) in [int, float]:
            return Vector2D(x = (self.x * other),
                            y = (self.y * other))
        if type(other) in [Vector2D]:
            return self.x*other.x + self.y*other.y

    #Set Reverse Multiplication to do the same thing as Forward Multiplication
    __rmul__ = __mul__
    
    #Scalar Division
    def __truediv__(self, num):
        return Vector2D(x = (self.x / float(num)),
                        y = (self.y / float(num)))
    
    def __neg__(self):
        return Vector2D(x = -1*self.x,
                        y = -1*self.y)

    #Call function, returns either x and y params or mag and dir params depending on option
    def __call__(self, mode = 'xy'):
        if self.x != None and self.y != None and mode == 'xy':
            return '('+str(round(self.x,4))+', '+str(round(self.y,4))+')'
        elif self.mag != None and self.dir != None and mode == 'md':
            return '('+str(round(self.mag,4))+', '+str(round(self.dir,4))+')'
        else:
            return 'ERROR: Vector properties not properly set.'

    #Print function, returns only x and y params
    def __str__(self):
        if self.x != None and self.y != None:
            return '('+str(round(self.x,4))+', '+str(round(self.y,4))+')'
        else:
            return 'ERROR: Vector properties not properly set.'
    __repr__ = __str__

if __name__ == '__main__':
    a = Vector2D(x=1, y=2)
    b = Vector2D(x=-1, y=5)
    c = -(b - 3*a)/2
    
    print(a, b)
    print(c)
    print(c('md'))
