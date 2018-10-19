import pygame
import pygame.event
from pygame.locals import *
from ParabolaClass import *

showGrid = True
showTicks = True
tickAmount = 10
#g = 9.8 #m/s^2
bP = (-1,-1) # Bad Point
m_pos = bP
mP1 = bP
mP2 = bP
mP3 = bP
axes = bP
doAssign = False
isClear = False
Dragging = False
posStatic = True

def inputLoop(screen):
    global doAssign,isClear,m_pos, showGrid, tickAmount, showTicks, Dragging, posStatic
    
    for event in pygame.event.get():
    #====================
    # WINDOW EVENTS
    #====================
        # Window Closed Event
        if event.type == QUIT:
            pygame.quit()
            return False
        # Window Resize Event
        elif event.type == VIDEORESIZE:
            old_surface_saved = screen
            screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
            # On the next line, if only part of the window
            # needs to be copied, there's some other options.
            screen.blit(old_surface_saved, (0,0))
            del old_surface_saved
    #====================
    # KEYBOARD EVENTS
    #====================
        # Key Released Events
        elif event.type == KEYUP:
            # Press ESCAPE to Quit
            if event.key == K_ESCAPE:
                pygame.quit()
                return False
            # Press SPACE to Show Grid
            elif event.key == K_SPACE:
                showGrid = not showGrid
            # Press UP ARROW to increase distance between grid lines
            elif event.key == K_UP:
                tickAmount += 10
                if (tickAmount > 500):
                    tickAmount = 10
            # Press DOWN ARROW to decrease distance between grid lines
            elif event.key == K_DOWN:
                tickAmount -= 10
                if (tickAmount < 10):
                    tickAmount = 10
            # Press T to show tick marks on axes
            elif event.key == K_t:
                showTicks = not showTicks
            # Press P to toggle between static and dynamic positioning of Parabola data
            elif event.key == K_p:
                posStatic = not posStatic
    #====================
    # MOUSE EVENTS
    #====================
        # While mouse is moving, keep track of mouse position
        elif event.type == MOUSEMOTION:
            m_pos = event.pos
        # MOUSEBUTTONDOWN events    
        elif event.type == MOUSEBUTTONDOWN:
            # Hold LEFT MOUSE BUTTON to Start Dragging
            if event.button == 1:
                # Turn on Dragging until left mouse RELEASED
                Dragging = True
                # And update position
                m_pos = event.pos
        # MOUSEBUTTONUP events
        elif event.type == MOUSEBUTTONUP:
            # Release RIGHT MOUSE BUTTON to Clear Screen
            if event.button == 3:
                # Clear all data
                isClear = True
            # Release LEFT MOUSE BUTTON to Stop Dragging and Assign this Point
            elif event.button == 1:
                # Save location to new point if necessary or update an old one??? 
                doAssign = True
                # Update mouse position
                m_pos = event.pos
                # Turn off Dragging
                Dragging = False
    #====================
    # UNKNOWN EVENTS
    #====================
        else:
            pass
            # print(event)
            # VIDEOEXPOSE
            #   App was "restored", possibly from taskbar or as part of VIDEORESIZE event
            # ACTIVEEVENT
            #   Gain:
            #       LOST_FOCUS        The application lost focus                  0x00
            #       GAIN_FOCUS        The application gained focus                0x01
            #   State:
            #       SDL_APPMOUSEFOCUS The application has mouse focus.            0x01
            #       SDL_APPINPUTFOCUS The application has keyboard focus          0x02
            #       SDL_APPACTIVE     The application is visible                  0x04



    return True
    
def main():
    global doAssign, isClear, m_pos, mP1, mP2, mP3, Dragging
    
    pygame.init()
    screen = pygame.display.set_mode( (700, 650) , RESIZABLE)
    pygame.display.set_caption('Parabola Sandbox')
    pygame.font.init()
    p1 = (350,350)
    p2 = (550,400)

    BLACK = (0, 0, 0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    BLUE = (0,0,255)
    GREEN = (0,255,0)
    PURPLE = (255, 0, 255)
    
    mP1=mP2=mP3=m_pos=bP
    while (inputLoop(screen)):
        screen.fill((255, 255, 255))
        if isClear:
            mP1=mP2=mP3=bP
            isClear = False
        else:
            drawAxesAndGrid(screen)
            if doAssign:
                if not ptOnScreen(screen,mP1):
                    mP1 = m_pos
                elif not ptOnScreen(screen,mP2):
                    mP2 = m_pos
                else:
                    mP3 = m_pos
                doAssign = False

            s1 = ptOnScreen(screen,mP1)
            s2 = ptOnScreen(screen,mP2)
            s3 = ptOnScreen(screen,mP3)
            sE = ptOnScreen(screen,m_pos)
            
            if s1 and s2:
                try:
                    if not Dragging and s3:
                        p = Parabola(mP1,mP2,mP3,2000)
                        drawParabola(screen,p,BLACK)
                        drawParabolaData(screen, p)
                    elif sE and Dragging:
                        p = Parabola(mP1,mP2,m_pos,2000)
                        drawParabola(screen,p,BLACK)
                        drawParabolaData(screen, p)
                except ValueError as e:
                    drawError(screen, e)
            
            # Only Drag one color
            if Dragging:
                if not s1:
                    color = GREEN
                elif not s2:
                    color = BLUE
                else:
                    color = RED
                if sE:
                    pygame.draw.circle(screen, color, m_pos, 5, 0)
                    
            # Paint other dots
            if s1:
                pygame.draw.circle(screen, GREEN, mP1, 5, 0)
            if s2:
                pygame.draw.circle(screen, BLUE, mP2, 5, 0)
            if s3 and not Dragging:
                pygame.draw.circle(screen, RED, mP3, 5, 0)
                
        pygame.display.update()
    pygame.quit()
    return
    
def ptOnScreen(screen, p):
    return (p[0] >= 0 and p[1] >= 0 and 
            p[0] <= screen.get_width() and p[1] <= screen.get_height())

def drawError(screen, e):
    drawPoint = (10,20)
    b = (0,0,0)
    w = (255,255,255)
    myfontS = pygame.font.SysFont('monospace', 16)
    Print1 = '{0}'.format(e)
    ts1 = myfontS.render(Print1, False, w)
    pygame.draw.rect(screen, b, (drawPoint[0], drawPoint[1], ts1.get_width(), ts1.get_height()))
    screen.blit(ts1,drawPoint)
    return

def drawParabolaData(screen, parabola):
    global m_pos,Dragging,mP3,posStatic,mP1
    
    angle = parabola.degrees
    if angle < 0:
        angle = -angle

    # Y is inverted in Game Graphics
    slope = -parabola.slope
    
    baseDrawPoint = (0,0)
    
    if posStatic:
        # If you want it stationary about the axes "origin", just make sure
        # it's not the same as the "last point" assigned
        #if parabola.known_points[0].astuple() != mP3:
        baseDrawPoint = (mP1[0]+75,mP1[1]+100)
        #else:
         #   baseDrawPoint = (parabola.known_points[1].x+75,parabola.known_points[1].y+100)
    else:
        # If you want it dynamically adjusted to be near the "dragging" point
        # Statement "if Dragging:" is unnecessary if you want it to be based off live mouse position
        # The if/else keeps it at the last assigned point while Dragging, and after assignment ('dropped')
        if Dragging:
            baseDrawPoint = (m_pos[0]+75,m_pos[1]+100)
        else:
            baseDrawPoint = (mP3[0]+75,mP3[1]+100)
        
    myfontS = pygame.font.SysFont('monospace', 12)
    Print1 = 'ANGLE {0:.2f} SLOPE {1:.2f}'.format(angle, slope)
    Print2 = '{0} {1} {2}'.format(parabola.known_points[0], parabola.known_points[1], parabola.known_points[2])
    Print3 = parabola.quadratic
    
    ts1 = myfontS.render(Print3, False, (0,0,0), (244,244,244))
    ts2 = myfontS.render(Print2, False, (0,0,0), (244,244,244))
    ts3 = myfontS.render(Print1, False, (0,0,0), (244,244,244))
    
    screen.blit(ts1,baseDrawPoint)
    screen.blit(ts2, (baseDrawPoint[0], baseDrawPoint[1] + ts1.get_height()))
    screen.blit(ts3, (baseDrawPoint[0], baseDrawPoint[1] + ts1.get_height() + ts2.get_height()))
    return

def drawParabola( screen, parabola, color ):
    pygame.draw.aalines(screen, color, False, parabola.get_list(), 0)
    return
    
def drawAxesAndGrid(screen):
    global showGrid, showTicks, tickAmount, mP1
    drawPoint = mP1
    
    if (not ptOnScreen(screen, drawPoint)):
        return

    b = (0,0,0)
    g = (223,223,223)
    
    for j in range(0, screen.get_height()):
        if ( (j - drawPoint[1]) % tickAmount == 0):
            if showGrid:
                pygame.draw.line(screen, g, (0, j), (screen.get_width(), j), 1)
            if showTicks:
                pygame.draw.line(screen, b, (drawPoint[0]-3, j), (drawPoint[0]+3,  j), 1)
            
    for i in range(0, screen.get_width()):
        if ( (i - drawPoint[0]) % tickAmount == 0):
            if showGrid:
                pygame.draw.line(screen, g, (i, 0), (i, screen.get_height()), 1)
            if showTicks:
                pygame.draw.line(screen, b, (i, drawPoint[1]-3), (i, drawPoint[1]+3), 1)

    pygame.draw.line(screen, b, (0     , drawPoint[1]), (screen.get_width(),  drawPoint[1]), 1)
    pygame.draw.line(screen, b, (drawPoint[0], 0     ), (drawPoint[0], screen.get_height()), 1)
        
    return

if __name__ == "__main__":
    main()
