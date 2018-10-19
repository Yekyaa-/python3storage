import pygame
import time
import pygame.event
from pygame.locals import *
from pygame import gfxdraw
import math
import numpy as np
import numpy.linalg as LA
import ParabolaClass

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

def calcEquation(p1,p2,v):
    # Avoid a singular matrix
    if (p1[0] == p2[0]):
        return 0,0,0,0,math.pi/2
        
    a = np.matrix([[ p1[0]**2, p1[0], 1 ],
               [ v[0]**2, v[0], 1 ],
               [ p2[0]**2, p2[0], 1]])
    b = np.matrix([ p1[1] , v[1], p2[1] ]).transpose()
    x = LA.solve(a,b)
    a,b,c=np.array(x).flatten().tolist()
    slope = 2*a *p1[0] + b
    angle = math.atan(slope)
    return a,b,c,slope,angle

def calcPoint(a,b,c,p1,p2,vertex,timeOffset):
    x = p1[0] + timeOffset
    y = x ** 2 * a + x * b + c
    # Translate to 0-ht pixels from original
    return (x,y)

def drawAngleSlope(screen, mP2, angle, slope):
    myfontS = pygame.font.SysFont('monospace', 14)
    Print1 = 'ANGLE {0:.2f} SLOPE {1:.2f}'.format(angle, slope)
    ts1 = myfontS.render(Print1, False, (0,0,0), (244,244,244))
    screen.blit(ts1,mP2)
    return
        
def drawSpecArc( screen, p1, p2, vertex, steps, color):
    swapped=False
    if (p2[0] < p1[0]):
        p1,p2=p2,p1
        swapped=True
    stepwidth = (p2[0]-p1[0])/steps
    a,b,c,slope,angle = calcEquation(p1,p2,vertex)
    array = []
    ht = screen.get_height()
    for i in range(0, steps+1):
        array.append(calcPoint(a,b,c,p1,p2,vertex,i*stepwidth))
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
    
def drawAxes(screen, mP1):
    BLACK = (0, 0, 0)

    pygame.draw.line(screen, BLACK, (0     , mP1[1]), (screen.get_width(),  mP1[1]), 1)
    pygame.draw.line(screen, BLACK, (mP1[0], 0     ), (mP1[0], screen.get_height()), 1)
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
            drawSpecArc( screen, mP1, mP2, vertex, 2000, BLACK)
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

def drawInfo(screen, mP1):
    myfontS = pygame.font.SysFont('monospace', 10)
    Print1 = '{0}'.format('Θ')
    ts1 = myfontS.render(Print1, False, (0,0,0))
    screen.blit(ts1,(mP1[0]+10,mP1[1]-15))
    return

main()
