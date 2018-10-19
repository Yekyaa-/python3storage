import pygame
import time
import pygame.event
from pygame.locals import *
from pygame import gfxdraw
import math
import numpy as np
import numpy.linalg as LA

showGrid = True
showTicks = True
tickAmount = 10
#g = 9.8 #m/s^2
bP = (-1,-1) # Bad Point
m_pos = bP
mP1 = bP
mP2 = bP
isSet = False
isClear = False
isMouseDown = False
def inputLoop(screen):
    global isSet,isClear,m_pos,isMouseDown, showGrid, tickAmount, showTicks
    
    for event in pygame.event.get():
        if (event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE)):
            pygame.quit()
            return False
        elif event.type == KEYUP:
            if event.key == K_SPACE:
                showGrid = not showGrid
            elif event.key == K_UP:
                tickAmount += 10
                if (tickAmount > 500):
                    tickAmount = 10
            elif event.key == K_DOWN:
                tickAmount -= 10
                if (tickAmount < 10):
                    tickAmount = 10
            elif event.key == K_t:
                showTicks = not showTicks
        elif event.type == MOUSEMOTION:
            m_pos = event.pos
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            isMouseDown = True
            m_pos = event.pos
        elif event.type == MOUSEBUTTONUP:
            if event.button == 3:
                isClear = True
            elif event.button == 1:
                isSet = True
                isMouseDown = False
                m_pos = event.pos
        elif event.type == pygame.VIDEORESIZE:
            old_surface_saved = screen
            screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
            # On the next line, if only part of the window
            # needs to be copied, there's some other options.
            screen.blit(old_surface_saved, (0,0))
            del old_surface_saved
    return True

def drawArc(screen, dAColor, p1, p2, r1, r2):
    # calculate angle between p1, p2
    # calculate velocity to reach p1, p2
    # 
    # for each THETA(O) between initial angle and final angle.
    #   calculateX and calculateY at given time(t)
    # or use x and y with Y value
    '''
    x(t) = t
    y(t) = - (- t * t + t + y(0) )
    
    v(f) = 0 = u * cos ( theta ) = arccos ( 1 / u )
    
    t = 0 when p1.x == p2.x 
    Want it to take same amount of time!!!
    x(2) == p2.x
    u * 2 * cos ( theta ) = ( p2.x - p1.x )
    u = ( p2.x - p1.x ) / ( 2 * cos( theta ) ) 
    u = ( p2.x - p1.x ) / ( time )
    '''
    
    
    return
def calcInitialVelocity( p1, p2, time, theta ):
    ''' Calculate initial velocity necessary to reach p2 from p1 at angle theta 
        o v_x(t) = u * cos( θ ) + ( a_x * t ) = u * cos( θ ) = u_x
        o v_y(t) = u * sin( θ ) + ( a_y * t )    
        v_y(time) = 0 = u * sin( theta ) + ( -g * time )
        v(0) = u = ( -g * time ) / sin( theta )
        t = 2 * v(0) * sin( theta ) / g
        v(0) = ( g * t ) / ( 2 * sin( theta ) )
        v(0) = ( p2[0] - p1[0] ) / time
        ( g * time ) / ( 2 * math.sin( theta ) )???? WTF***
        
        x = v_x(0) * t;  p2[0] = u * cos( theta ) * time + p1[0]
        u = ( p2[0] - p1[0] ) / ( time * math.cos( theta ) )
    '''
    v_x = ( p2[0] - p1[0] ) / ( time * math.cos( theta ) )
    v_y = ( p2[1] - p1[1] ) / ( time * math.sin( theta ) )
    return math.sqrt( v_x ** 2 + v_y ** 2 )

def graph(p1,p2,time,maxtime):
    perc = time / maxtime
    x_t = (p2[0]-p1[0]) * perc + p1[0]
    #y_t = p1[1] + 0.5 * ( -g * 
    return
def calcPoint( p1, p2, time, steps, theta ):
    #u = calcInitialVelocity( p1, p2, maxtime, theta )
    # y = ax^2 + bx + c
    # a = -g (open downward)
    # c = p1[1]
    # time = step_number * 
    t = (time/steps)
    x_t = t*(p2[0]-p1[0])              + p1[0]
    y_t = -(-t*t+t) * (p2[1]-p1[1])**2 + p1[1]
    '''
    x-intercepts :
        0 = -gx^2 + bx + p1[1]
    '''
    return ( round( x_t ) , round( y_t ) )

''' working on coordinate system
p1 = (0,0), so everything is -p1[0] or -p1[1]
p2 = endpoint

''' 
def calcEquation2(p1,p2,v):
    if (p1[0] == p2[0]):
        return 0,0,0,0,0
    a = np.matrix([[ p1[0]**2, p1[0], 1 ],
               [ v[0]**2, v[0], 1 ],
               [ p2[0]**2, p2[0], 1]])
    b = np.matrix([ p1[1] , v[1], p2[1] ]).transpose()
    x = LA.solve(a,b)
    a,b,c=np.array(x).flatten().tolist()
    slope = 2*a *p1[0] + b
    angle = math.atan(slope)
    return a,b,c,slope,angle

def calcPoint3(ht, a,b,c,p1,p2,vertex,i,stepwidth):
    x = p1[0] + i * stepwidth
    y = x ** 2 * a + x * b + c
    # Translate to 0-ht pixels from original
    return (x,y)

def drawAngleSlope(screen, mP2, angle, slope):
    myfontS = pygame.font.SysFont('monospace', 14)
    Print1 = 'ANGLE {0:.2f} SLOPE {1:.2f}'.format(angle, slope)
    ts1 = myfontS.render(Print1, False, (0,0,0), (244,244,244))
    screen.blit(ts1,mP2)
    return
    
    
def drawSpecArc3( screen, p1, p2, vertex, steps, color):
    swapped=False
    if (p2[0] < p1[0]):
        p1,p2=p2,p1
        swapped=True
    # 
    stepwidth = (p2[0]-p1[0])/steps
    a,b,c,slope,angle = calcEquation2(p1,p2,vertex)
    array = []
    ht = screen.get_height()
    for i in range(0, steps+1):
        array.append(calcPoint3(ht,a,b,c,p1,p2,vertex,i,stepwidth))
    pygame.draw.aalines(screen, color, False, array, 0)
    angle = math.fabs(math.degrees(angle))
    if (not swapped):
        slope = -slope
        #angle = -angle
        drawPoint = (p1[0]+150,p1[1]-200)
    else:
        drawPoint = (p2[0]+150,p2[1]-200)
    drawAngleSlope(screen, drawPoint, angle, slope)
    return
    
def drawSpecArc2( screen, p1, p2, steps, color ):
    array = []
    for i in range( 0, steps+1):
        array.append(calcPoint2(p1,p2,i,steps))
    pygame.draw.aalines(screen, color, False, array, 0)
    return
    
isPrinted = False
def drawSpecArc( screen, p1, p2, steps, color ):
    global isPrinted
    prevPoint = p1

    for i in range( 0, steps+1 ):
        #x, y = calcPoint( p1, p2, i, steps, theta )
        #pygame.draw.circle(screen, color, (x, y), 3, 0)
        x,y =calcPoint2(p1,p2,i,steps)
        if (x >= 0) and (x <= screen.get_width()) and (y >= 0) and (y <= screen.get_height()):
            #pygame.draw.circle(screen, color, (x,y), 1, 0)
            pygame.gfxdraw.pixel(screen, x, y, color)
            #pygame.draw.line(screen,color,prevPoint,(x,y))
        prevPoint = (x,y)
    isPrinted = True
    return
    
def drawHelp(screen, p1, p2, angle, velocity):
    ''' 
        Initial launch angle, θ = θ_i*** IN RADIANS ***

        Vertical Acceleration, a
        o a_y = -g
        o   o The acceleration, a, in the vertical direction is just due to gravity (free fall)
        
        Horizontal Acceleration, a_x
        o a_x = 0
        o   o In projectile motion, there is no acceleration in the horizontal direction.

        Initial velocity, u
        o u = v(0)
        o u_x = v_x(0) = u * cos( θ )
        o u_y = v_y(0) = u * sin( θ )
        o The initial velocity can be expressed as x components and y components

        x(t) == p2.x = final time
        
        Velocity at time t, v(t)
        o v(t) = math.sqrt( v_x(t) ** 2 + v_y(t) ** 2 )
        o v_x(t) = u * cos( θ ) + ( a_x * t ) = u * cos( θ ) = u_x
        o v_y(t) = u * sin( θ ) + ( a_y * t )
        
        Time of flight, T
        o T = ( 2 * u * sin( θ ) ) / g
        o The time of flight of an object, given the initial launch angle and initial velocity
        
        Time to Max Height, T_h
        o T = ( u * sin( θ ) ) / g        
        
        Displacement at time t, Magnitude, d(t)
        o d(t) = delta_r = math.sqrt( x(t) ** 2 + y(t) ** 2 )
        
        Horizontal Displacement, x(t)
        o x(t) = u * t * cos( θ ) + 0.5 * a_x * t * t + x(0)

        Range, R
        o R( u , θ ) = ( u * u * sin( 2 * θ ) ) / g
        o The range of an object, given the initial launch angle and initial velocity
        o The horizontal displacement of the projectile is called the range of the projectile 
          and depends on the initial velocity of the object

        Vertical Displacement, y(t)
        o y(t) = u * t * sin( θ ) + 0.5 * (a_x = -g) * t * t + y(0)
        
        Maximum height, H
        o H( u , θ ) = ( u * u * sin( θ ) * sin( θ ) ) / ( 2 * g )
        o The maximum height of an object, given the initial launch angle and initial velocity
        
        Angle of Reach, Z = θ_f *** IN RADIANS ***
        o Z = 0.5 * math.arcsin( ( g * d ) / ( v * v ) )
        o Z = θ_f
        o The angle of reach is the angle the object must be launched at in order to achieve a specific distance
    '''
    return
isClear = False

def drawAxes(screen, mP1):
    BLACK = (0, 0, 0)

    pygame.draw.line(screen, BLACK, (0     , mP1[1]), (screen.get_width(),  mP1[1]), 1)
    pygame.draw.line(screen, BLACK, (mP1[0], 0     ), (mP1[0], screen.get_height()), 1)
    #pygame.draw.circle(screen, (0,0,0), mP1, 50, 1)
    
    #pygame.draw.arc(screen, (0,0,0),
    #    ((mP1[0] - 60, mP1[1] - 60), (120, 120)),
    #    0, math.pi/4, 1)
    #pygame.draw.arc(screen, (0,128,128),
    #    ((mP1[0], mP1[1]), (400, 25)),
    #    0,math.pi,1)
    #pygame.draw.rect(screen, c,
    #((mP1[0] - 70, mP1[1] - 70), (140, 140)), 1)
    return

def drawGrid(screen, mP1):
    if (mP1 == bP):
        return
    global showGrid, showTicks, tickAmount
    c = (0,0,0)
    g = (223,223,223)
    
    for j in range(0, screen.get_height()):
        if ( (j - mP1[1]) % tickAmount == 0):
            if showGrid:
                pygame.draw.line(screen, g, (0, j), (screen.get_width(), j), 1)
            if showTicks:
                pygame.draw.line(screen, c, (mP1[0]-3, j), (mP1[0]+3,  j), 1)
            
    for i in range(0, screen.get_width()):
        if ( (i - mP1[0]) % tickAmount == 0):
            if showGrid:
                pygame.draw.line(screen, g, (i, 0), (i, screen.get_height()), 1)
            if showTicks:
                pygame.draw.line(screen, c, (i, mP1[1]-3), (i, mP1[1]+3), 1)
    return

def main():
    global isSet, isClear, m_pos, mP1, mP2, isMouseDown
    
    pygame.init()
    screen = pygame.display.set_mode( (700, 650) , RESIZABLE)
    pygame.display.set_caption('Some Math Stuff')
    pygame.font.init()
    p1 = (350,350)
    p2 = (550,400)
    #a1,a2 = angleToHit(p1,p2,200)
    BLACK = (0, 0, 0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    BLUE = (0,0,255)
    GREEN = (0,255,0)
    mP1=mP2=m_pos=bP
    while (inputLoop(screen)):
        screen.fill((255, 255, 255))
        drawGrid(screen, mP1)
        drawAxes(screen, mP1)        
        if isMouseDown:
            if (ptOnScreen(mP1,screen)):
                mP2 = m_pos
        if isClear:
            mP1 = bP
            mP2 = bP
            isClear = False
        elif isSet:
            if not ptOnScreen(mP1, screen):
                mP1 = m_pos
            elif not ptOnScreen(mP2, screen):
                mP2 = m_pos
            isSet = False
        elif mP1!=mP2 and ptOnScreen(mP1,screen) and ptOnScreen(mP2,screen):

            if (mP1[1] < mP2[1]):
                vertex_x=math.fabs((mP2[0]-mP1[0])/2 + mP1[0])
                vertex_y = mP1[1]-100
            else:
                vertex_x=math.fabs((mP2[0]-mP1[0])/2 + mP1[0])
                vertex_y= mP2[1]-100
            vertex=(vertex_x, vertex_y)
            drawSpecArc3( screen, mP1, mP2, vertex, 2000, BLACK)
            #drawSpecArc2( screen, mP1, mP2, 2000, BLACK )
            #drawSpecArc( screen, (mP1[0]+20,mP1[1]+20), (mP2[0]+20,mP2[1]+20), 2000, RED )
        if (ptOnScreen(mP1,screen)):
            pygame.draw.circle(screen, GREEN, mP1, 5, 0)
        if (ptOnScreen(mP2, screen)):
            pygame.draw.circle(screen, RED, mP2, 5, 0)
        drawInfo(screen,mP1)
        pygame.display.update()
    pygame.quit()
    return
def ptOnScreen(p, screen):
    return (p[0] >= 0 and p[1] >= 0 and 
            p[0] <= screen.get_width() and p[1] <= screen.get_height())
def between(min, x, max):
    return (x >= min) and (x <= max)
def distance(Point1,Point2):
    return math.sqrt((Point2[1]-Point1[1]) ** 2 + (Point2[0]-Point1[0]) ** 2)
    

def midpoint(Point1, Point2):
    return ((Point2[0]-Point1[0])/2,(Point2[1]-Point1[1])/2)

def iVelocity(speed, angle):
    return (speed * math.cos(angle), speed * math.sin(angle))
    
def timeOfFlight(speed, angle, inclineangle=0):
    return (2*speed*math.sin(angle - inclineangle) / (g * math.cos(inclineangle)))

def angleToHit(src, dst, speed):
    v2 = speed*speed
    x = src[0] - dst[0]
    y = src[1] - dst[1]
    first = math.atan((v2 - math.sqrt( v2*v2 - g * (g * x * x + 2 * y * v2) )) / (g * x))
    second = math.atan((v2 + math.sqrt( v2*v2 - g * (g * x * x + 2 * y * v2) )) / (g * x))
    return math.degrees(first), math.degrees(second)

def angleBetweenPts(p1, p2):
    return math.atan2(p1[1]-p2[1],p1[0]-p2[0])

def x(counter, steps, p1, p2):
    a,b,w,z=calcEquation(p1,p2)
    # Range = P2.X - P1.X
    range = p2[0] - p1[0]
    # t = ThisStep/MaxSteps
    t = counter / steps
    
    # x = t
    _x = w * t + a
    
    return ( _x ) # * range + p1[0]

def y(counter, steps, p1, p2):
    a,b,w,z=calcEquation(p1,p2)
    # Range = P2.X - P1.X
    range = p2[0] - p1[0]
    # t = ThisStep/MaxSteps
    t = counter/steps

    # y = -(-t^2+t-1) = t^2 - t + b
    # y = -t^2 + z*t + b
    _y = -(-t ** 2 + z * t - b)
    
    return ( _y ) # * range + p1[1] )
    
def calcEquation(p1,p2,amp=1):
    scale_x = 1
    scale_y = 1
    scale_z = 1
    
    a=b=w=z=0
    # t = 0,1
    if p2[0] == p1[0] and p2[1] == p1[1]:
        return

    range = p2[0] - p1[0]

    # x = t
    # y = -t^2 + t
    # x = a + w * t
    # x = a + w * t    (x = t, still has a "w" and an "a")
    # y = -(-t^2+t-1) = t^2 - t + b
    # y = -t^2 + z*t + b
    # y = (t**2 - z * t + b)*amp
    # @ t=0 => a = x(0)
    # @ t=0 => b = y(0)
    a = p1[0]/range
    b = p1[1]/range
    # @ t=1 => w = x(1)-a
    # @ t=1 => y = amp  - amp*z + b; z = (amp + b - y(1))/amp
    w = p2[0]/range - a
    z = (1 + b) - p2[1]/range
    return a,b,w,z

def drawInfo(screen, mP1):
    myfontS = pygame.font.SysFont('monospace', 10)
    Print1 = '{0}'.format('Θ')
    ts1 = myfontS.render(Print1, False, (0,0,0))
    screen.blit(ts1,(mP1[0]+10,mP1[1]-15))
    return
    
def calcPoint2( p1, p2, counter, steps ):
    if p2[0] == p1[0] and p2[1] == p1[1]:
        return (0,0)

    if p1[0] > p2[0]:
        p1,p2=p2,p1
    # Range = P2.X - P1.X
    range = p2[0] - p1[0]

    if (range == 0) :
        return (0,0)
    amp = 1
    a,b,w,z = calcEquation(p1,p2)

    
    # t = ThisStep/MaxSteps
    _t = counter / steps
    # x = t
    x_t = ( w * _t + a ) * range
    #_t *= range
    # y = -(-t^2+t-1) = t^2 - t + b
    # _t = (x_t - a) / w
    # y = (x^2 - 2ax + a^2) / w^2 - xz/w + az/w + bx/w - ax/w
    # y = 1/w^2 (x^2 -2ax +a^2 - xzw + azw + bxw - axw
    y_t = ( _t*_t -  z * _t  + b ) * range
    #t = (time/steps)
    #x_t = t*(p2[0]-p1[0])              + p1[0]
    #y_t = -(-t*t+t) * (p2[1]-p1[1])**2 + p1[1]
    slope = 2 * a / (w*w)
    rad = math.atan(slope)
    deg = math.degrees(rad)
    #print('slope = {0:.2f} arctan(slope)={1:.2f} angle={2:.2f}'.format(slope, rad,deg))
    # ( w * _t + a ) ^2
    return ( round( x_t ) , round( y_t ) )

'''
    P1 = (-2, 3), P2 = ( 3, 6)
    
    x = a_1 + w * t
    y = -t^2 + z*t + b_1
    
    t = 0, x = -2, y = 3
    t = 1, x = 3, y = 6
    
    x = a_1 = -2, a_1 = -2@t=0
    b_1 = 3@t=0
    
    x = -2 + w * t
    y = -t^2 +z*t + 3
    (sub in P2)
    x:
    3 = -2 + w * t =>  5 = w * t ==> w = 5 @t=1
    y:
    -t^2+z*t +3=6 => -t^2 + z*t -3 = 0 ==> -1 + z - 3 ==> z = 4@t==1
    t^2 - z*t +3 = 0 ==> 1 - z + 3 = 0 ==> z = 4 @ t==1
    y = -t^2 +4*t + 3
    (-b +- sqrt(b^2 - 4ac) ) / 2*a WHERE a=(-1), b = (z), c = -3
p1 = (50,10)
p2 = (-50,-20)
P1 = (-1,3)
P2 = (3,4)
    
'''

def dofor(p1,p2,Steps):    
    for expanded_t in range(0, Steps+1):
        print('{0:.4f} ({1:.4f},{2:.4f}) : {3}'.format(expanded_t/Steps, x(expanded_t,Steps,p1,p2), y(expanded_t,Steps,p1,p2), calcPoint2(p1,p2,expanded_t,Steps)))
    return

p1=(350,350)
p2=(550,325)
Steps = 22
#t_0 = 0
#t_1 = 1
# p2.x - p1.x
Range = p2[0] - p1[0]
#WidthPerStep = Range / Steps

#dofor(p1,p2,Steps)    
main()