'''
Parabola:

Point 1 (x1,y1)
Point 2 (x2,y2)
f(x)=ax^2+bx+c
f(x1) = y1 = a*x1^2+b*x1+c
f(x2) = y2 = a*x2^2+b*x2+c


To find the slope, take the derivative with respect to x.

d/dx(ax^2+bx+c)

=d/dx(ax^2)+d/dx(bx)+d/dx(c)
=2ax+b.
if (x == 0):
    slope = b
'''
import numpy as np
import numpy.linalg as LA
import math

P1 = (150, 350)
P2 = (550, 375)
'''
 f(150) = 350 = a*(150)^2 + 150*b + c
 f(550) = 375 = a*(550)^2 + 550*b + c
rng = (P2[0]-P1[0])
a = np.matrix([
                [P1[0]**2,P1[0],1],
                [P2[0]**2,P2[0],1]
                #,[rng**2,rng,1]
            ])
b = np.matrix([P1[1] , P2[1]]) #, P1[1] + 200])
'''


def f(p1,p2,v):
    a = np.matrix([[ p1[0]**2, p1[0], 1 ],
               [ v[0]**2, v[0], 1 ],
               [ p2[0]**2, p2[0], 1]])
    b = np.matrix([ p1[1] , v[1], p2[1] ]).transpose()
    x = LA.solve(a,b)
    x1,x2,x3=np.array(x).flatten().tolist()
    print() #print(x1,x2,x3)
    print('p1={0},p2={1},vertex={2}'.format(p1,p2,v))
    print('y= {0:.6f} x^2 + {1:.6f} x + {2:.6f}'\
          ' where x = [{3}, {4}, {5}]'.format(x1,x2,x3, p1[0],v[0],p2[0]))
    slope = 2*x1 *p1[0] + x2
    rad = math.atan(slope)
    deg = math.degrees(rad)
    print('slope = {0} angle= {1:.2f} degrees {2:.2f} radians'.format(slope, deg, rad))
    printPtLst(p1,p2,v,
    return
def printPtLst(p1, p2, vertex, steps):
    if (p2[0] < p1[0]):
        p1,p2=p2,p1
    # 
    stepwidth = (p2[0]-p1[0])/steps
    a,b,c,slope,angle = calcEquation2(p1,p2,vertex)
    array = []
    for i in range(0, steps+1):
        print(calcPoint3(0,a,-b,c,p1,p2,vertex,i,stepwidth))
    print()
    #pygame.draw.aalines(screen, color, False, array, 0)
    return
    
def calcPoint3(ht, a,b,c,p1,p2,vertex,i,stepwidth):
    x = p1[0] + i * stepwidth
    y = x ** 2 * a + x * b + c
    # Translate to 0-ht pixels from original
    return (x,y)
    
p1=(0,-1)
p2=(10,-3)
v=(11,-5)
f(p1,p2,v)
p1=(150,350)
p2=(400,100)
v=(200,150)
f(p1,p2,v)
p1=(350,350)
p2=(550,400)
v=(math.fabs((p2[0]-p1[0])/2 + p1[0]), p1[1]+100)
printPtLst(p1,p2,v,20)
