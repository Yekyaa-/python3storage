import math
import numpy as np
import numpy.linalg as LA

class Point3D:
    @classmethod
    def fromtuple(cls, tup):
        return cls(tup[0], tup[1], tup[2])
        
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __repr__(self):
        return "<Point3D( x:{0:7.2f}, y:{1:7.2f}, z:{2:7.2f})>".format(self.x,self.y,self.z)
        
    def __str__(self):
        return "({0:7.2f}, {1:7.2f}, {2:7.2f})".format(self.x, self.y, self.z)
        
class Parabola3D:
    # Straight lines require 2 points,
    # Anything in a plane requires at least 3.
    def __init__(self, p1, p2, p3, steps):
        if (p1 == p2 or p2 == p3 or p1 == p3):
            raise ValueError("Parabola requires three unique points!")

        pt_array = [Point3D.fromtuple(p1), Point3D.fromtuple(p2), Point3D.fromtuple(p3)]
        pt_array.sort(key = lambda point: point.x)
        self.known_points = pt_array
        self.angle = math.pi / 2
        self.slope = 0
        self.change_steps(steps)
        self.quadratic = self.equation()

    def change_steps(self, steps):
        self.steps = steps
        self.stepwidth = ( self.known_points[len(self.known_points)-1].x - self.known_points[0].x ) / steps
        self.quadratic = self.equation()
        self.generate_list()
        
    def equation(self):
        p1 = self.known_points[0]
        p2 = self.known_points[1]
        p3 = self.known_points[2]
        
        _A = np.matrix([[ p1.x**2, p1.x, 1 ],
                   [ p2.x**2, p2.x, 1 ],
                   [ p3.x**2, p3.x, 1]])
        _b = np.matrix([ p1.y , p2.y, p3.y ]).transpose()
        _x = LA.solve(_A,_b)
        
        self.a,self.b,self.c = np.array(_x).flatten().tolist()
        self.slope = 2 * self.a * self.known_points[0].x + self.b
        self.angle = math.atan(self.slope)
        return "y ={0:8.2f} x\xB2 +{1:8.2f} x +{2:8.2f}".format(self.a, self.b, self.c)
        
    def step(self, num):
        x = self.known_points[0].x + num * self.stepwidth
        y = x ** 2 * self.a + x * self.b + self.c
        z = - x ** 2 - y ** 2 + 6
        return Point3D( x, y, z )

    def generate_list(self):
        the_list = []
        for i in range(0, self.steps+1):
            the_list.append(self.step(i))
        #angle = math.fabs(math.degrees(angle))
        #if (not swapped):
        #    slope = -slope
        self.point_list = the_list
        return

p = Parabola3D((150,0,35), (300,-300,75), (450,0,85), 20)
for c in p.point_list:
    print(c)
print(p.step(21))
print(p.quadratic,end='\n\n')
p.change_steps(10)
for c in p.point_list:
    print(c)
print(p.step(11))
print(p.quadratic,end='\n\n')
print(p.known_points)
print(p.slope, p.angle, math.degrees(p.angle))

p = Parabola3D((150,0,0),(0,0,100),(150,0,0),20)
