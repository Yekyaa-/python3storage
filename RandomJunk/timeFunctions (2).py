import pygame
import time
import pygame.event
from pygame.locals import *
import math

g = 9.8 #m/s^2

def inputLoop():
    for event in pygame.event.get():
        if (event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE)):
            pygame.quit()
            return False
    return True

def drawArc(screen, dAColor, p1, p2, r1, r2):
    # calculate angle between p1, p2
    # calculate velocity to reach p1, p2
    # 
    # for each THETA(O) between initial angle and final angle.
    #   calculateX and calculateY at given time(t)
    # or use x and y with Y value
    '''
    x(t) = u * t * cos( θ ) + 0.5 * a_x * t * t + x(0)
    y(t) = u * t * sin( θ ) + 0.5 * (a_x = -g) * t * t + y(0)
    
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
def calcPoint( p1, p2, time, maxtime, theta ):
    u = calcInitialVelocity( p1, p2, maxtime, theta )
    # y = ax^2 + bx + c
    # a = -g (open downward)
    # c = p1[1]
    # 
    perc = ( time / maxtime )
    H = p1[1] + 3
    b = H * 2 * -g
    x_t = ( p2[0] - p1[0] ) * perc + p1[0]
    #y_t = -( p2[1] - p1[1] ) * perc + p1[1] - maxtime
    #y_t = -g * x_t ** 2 + b * x_t + p1[1]
    y_t = -g * ((x_t - b) ** 2) + p1[1]
    #y_t = math.tan( theta ) * x_t - ( 0.5 * g * x_t * x_t ) / ( ( u * math.cos( theta ) ) ** 2 )
    #x_t = u * time * math.cos( theta ) + p1[0]
    #y_t = -g * x_t ** 2 + b*x_t + p1[1]
    #( p2[1] - p1[1] ) - 0.5 * ( g ) * ( perc * perc )
    y_t = -g* x_t**2 + p1[1]
    '''
    x-intercepts :
        0 = -gx^2 + bx + p1[1]
    '''
    return ( round( x_t ) , round( y_t ) )

''' working on coordinate system
p1 = (0,0), so everything is -p1[0] or -p1[1]
p2 = endpoint

'''    
isPrinted = False
def drawSpecArc( screen, p1, p2, theta, steps, color ):    
    global isPrinted
    for i in range( 0, steps ):
        x, y = calcPoint( p1, p2, i+1, steps, theta )
        pygame.draw.circle(screen, color, (x, y), 3, 0)
        if not isPrinted:
            print( [ x, y ] )
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
    
def main():
    pygame.init()
    screen = pygame.display.set_mode( (700, 650) )
    pygame.display.set_caption('Some Math Stuff')
    pygame.font.init()
    p1 = (150,350)
    p2 = (575,250)
    a1,a2 = angleToHit(p1,p2,200)
    BLACK = (0, 0, 0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    BLUE = (0,0,255)
    GREEN = (0,255,0)
    while (inputLoop()):
        screen.fill((255, 255, 255))
        drawSpecArc( screen, p1, p2, math.radians( -85 ), 300, BLUE )
        pygame.draw.circle(screen, GREEN, p1, 3, 0)
        pygame.draw.circle(screen, RED, p2, 3, 0)
        #for i in range(0,360):
         #   pass
            #x = 
            #pygame.draw.circle(screen,BLUE,
        #pygame.draw.arc(screen, BLACK, (p1, p2), math.pi/2, 3*math.pi/2, 5)        
        #pygame.draw.arc(screen, BLUE, (p1, p2), 0, math.pi/2, 5)        
        pygame.display.update()
    pygame.quit()
    return
    
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
p1 = (50,10)
p2 = (-50,-20)
P1 = (-1,3)
P2 = (3,4)
print('angleBetweenPts=',math.degrees(angleBetweenPts(p1,p2)))
print(p1,p2,'dist=',distance(p1,p2))
print(P1,P2,'dist=',distance(P1,P2))
print(P1,P2,'midpoint=',midpoint((-1,1),(3,4)))
print(math.radians(45))
print(iVelocity(200,math.radians(45)))
print(timeOfFlight(200, math.radians(45)))
print(timeOfFlight(200, math.radians(45), math.radians(30)))
a1,a2 = angleToHit(p1,p2,200)
print(a1,a2)
print(timeOfFlight(200, math.radians(a1)), timeOfFlight(200, math.radians(a2)))
main()