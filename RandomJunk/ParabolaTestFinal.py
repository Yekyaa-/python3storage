import pygame
import pygame.event
from pygame.locals import *
from ParabolaClass import *

class Colors:
    BLACK =     (  0,  0,  0)
    RED =       (255,  0,  0)
    DARKRED =   (127,  0,  0)
    GREEN =     (  0,255,  0)
    DARKGREEN = (  0,127,  0)
    BLUE =      (  0,  0,255)
    DARKBLUE =  (  0,  0,127)
    PURPLE =    (255,  0,255)
    DARKPURPLE =(127,  0,127)
    LIGHTGRAY = (223,223,223)
    TEXTGRAY =  (244,244,244)
    WHITE =     (255,255,255)
    
class ParabolaTest:
    def resize(self, event):
        old_surface_saved = self.screen
        self.screen = pygame.display.set_mode((event.w, event.h),
                                          pygame.RESIZABLE)
        self.topLeft        = (      0,       0)
        self.topRight       = (event.w,       0)
        self.bottomLeft     = (      0, event.h)
        self.bottomRight    = (event.w, event.h)
        self.width          = event.w
        self.height         = event.h
        # On the next line, if only part of the window
        # needs to be copied, there's some other options.
        self.screen.blit(old_surface_saved, self.topLeft)
        del old_surface_saved
    
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.Clock = pygame.time.Clock()
        self.width = 700
        self.height = 650
        self.screen = pygame.display.set_mode( (self.width, self.height) , RESIZABLE)
        pygame.display.set_caption('Parabola Sandbox')
        self.parabolaCounter = 1
        self.drawBoundingBox = False
        self.BIT_CENTER_ON_Y = 1
        self.BIT_CENTER_ON_X = 2
        self.BIT_WIDE_BG = 4
        self.BIT_TALL_BG = 8
        self.errorDisplayMode = self.BIT_CENTER_ON_X | self.BIT_CENTER_ON_Y | self.BIT_WIDE_BG
        self.fpsDisplayMode = self.BIT_CENTER_ON_X | self.BIT_WIDE_BG
        self.showSteps = True
        self.showFPS = True
        self.reCalculate = False
        self.screenFillColor = Colors.WHITE
        self.errorBackColor = Colors.BLACK
        self.errorTextColor = Colors.WHITE
        self.parabolaDataTextColor = Colors.BLACK
        self.parabolaDataBackColor = Colors.TEXTGRAY
        self.mousePositionTextColor = Colors.BLACK
        self.mousePositionBackColor = Colors.TEXTGRAY
        self.axesColor = Colors.BLACK
        self.parabolaColor = Colors.BLACK
        self.parabolaStepMax = 200
        self.parabolaStepMin = 2
        self.parabolaStepDelta = 1
        self.point1Color = Colors.DARKGREEN
        self.point2Color = Colors.DARKBLUE
        self.point3Color = Colors.DARKRED
        self.draggingPointColor = Colors.PURPLE
        self.gridColor = Colors.LIGHTGRAY
        self.tickColor = Colors.BLACK
        self.infoPadding = 1
        self.infoFontSize = 12
        self.isInfoStatic = True
        self.staticOffsetX = 20
        self.staticOffsetY = 20
        self.dynamicOffsetX = 20
        self.dynamicOffsetY = 20
        self.parabola = None
        self.errorFontSize = 16
        self.errorPoint = (10,20)
        
        self.doAssign = False
        self.doReset = False
        self.isDragging = False

        self.showGrid = True
        self.showTicks = True
        self.tickDrawSize = 6
        self.currentTickDistance = 20
        self.tickAmount = 10
        self.minTickSize = 10
        self.maxTickSize = 500

        self.pointRadius = 5
        self.parabolaStepCount = 25

        self.topLeft        = (         0,           0)
        self.topRight       = (self.width,           0)
        self.bottomLeft     = (         0, self.height)
        self.bottomRight    = (self.width, self.height)
        
        self.badPoint       = (      None,        None)
        self.point1 = self.point2 = self.point3 = self.badPoint
        self.axes = self.mouse_position = self.badPoint

    def inputLoop(self,screen):
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
                self.resize(event)
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
                    self.toggleGrid()
                # Press UP ARROW to increase distance between grid lines
                elif event.key == K_UP:
                    self.increaseTickAmount()
                # Press DOWN ARROW to decrease distance between grid lines
                elif event.key == K_DOWN:
                    self.decreaseTickAmount()
                elif event.key == K_b:
                    self.drawBoundingBox = not self.drawBoundingBox
                # Press T to show tick marks on axes
                elif event.key == K_t:
                    self.toggleTicks()
                # Press P to toggle between static and dynamic positioning of Parabola data
                elif event.key == K_p:
                    self.toggleStatic()
                elif event.key == K_f:
                    self.toggleFPS()
                #elif event.key == K_e:
                #    self.nextErrorMode()
                elif event.key == K_s:
                    self.showSteps = not self.showSteps
                elif event.key == K_c:
                    self.parabolaCounter += 1
                    if (self.parabolaCounter > 3):
                        self.parabolaCounter = 1
        #====================
        # MOUSE EVENTS
        #====================
            # While mouse is moving, keep track of mouse position
            elif event.type == MOUSEMOTION:
                self.updateMousePosition(event)
            # MOUSEBUTTONDOWN events    
            elif event.type == MOUSEBUTTONDOWN:
                # Hold LEFT MOUSE BUTTON to Start Dragging
                if self.isLMB(event.button):
                    # Turn on Dragging until left mouse RELEASED
                    self.isDragging = True
                    # And update position
                    self.updateMousePosition(event)
                else:
                    #print(event)
                    pass
            # MOUSEBUTTONUP events
            elif event.type == MOUSEBUTTONUP:
                # Release RIGHT MOUSE BUTTON to Clear Screen
                if self.isRMB(event.button):
                    # Clear all data
                    self.doReset = True
                # Release LEFT MOUSE BUTTON to Stop Dragging and Assign this Point
                elif self.isLMB(event.button):
                    # Save location to new point if necessary or update an old one??? 
                    self.doAssign = True
                    # Update mouse position
                    self.updateMousePosition(event)
                    # Turn off Dragging
                    self.isDragging = False
                elif self.isMouseWheelUp(event.button):
                    self.increaseStepAmount()
                elif self.isMouseWheelDown(event.button):
                    self.decreaseStepAmount()
                    #self.decreaseTickAmount()
                elif self.isMMB(event.button):
                    self.toggleGrid()
                else:
                    # print(event)
                    pass
        #====================
        # UNKNOWN EVENTS
        #====================
            else:
                # print(event)
                pass
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
        
    def run(self):
        while (self.inputLoop(self.screen)):
            self.Clock.tick()
            self.screen.fill(self.screenFillColor)
            if self.doReset:
                self.point1 = self.point2 = self.point3 = self.badPoint
                self.doReset = False
            else:
                if self.doAssign:
                    if not self.isPointOnScreen(self.point1):
                        self.point1 = self.mouse_position
                    elif not self.isPointOnScreen(self.point2):
                        self.point2 = self.mouse_position
                    else:
                        self.point3 = self.mouse_position
                    self.doAssign = False

                s1 = self.isPointOnScreen(self.point1)
                s2 = self.isPointOnScreen(self.point2)
                s3 = self.isPointOnScreen(self.point3)
                sE = self.isPointOnScreen(self.mouse_position)

                if not s1 and sE and self.isDragging:
                    self.drawAxesAndGrid(self.mouse_position)
                else:
                    self.drawAxesAndGrid(self.point1)
                    
                # Require Points 1 & 2 with either Point 3 set, or currently being placed to draw Parabola
                if s1 and s2:
                    try:
                        if not self.isDragging and s3:
                            if self.parabola == None or self.reCalculate:
                                self.parabola = Parabola(self.point1,self.point2,self.point3,self.parabolaStepCount)
                                self.reCalculate = False
                            self.drawParabola()
                            self.drawParabolaData()
                        elif self.isDragging and sE:
                            self.parabola = Parabola(self.point1,self.point2,self.mouse_position,self.parabolaStepCount)
                            self.drawParabola()
                            self.drawParabolaData()
                    except ValueError as e:
                        del self.parabola
                        self.parabola = None
                        self.drawErrorData(e)
                
                # Only Drag one point at a time
                if self.isDragging:
                    # If first point not set, drag it
                    if not s1:
                        color = self.point1Color
                    # If second point not set, drag it
                    elif not s2:
                        color = self.point2Color
                    # If third point not set, drag it
                    elif not s3:
                        color = self.point3Color
                    # All dots assigned, drag "new position" of third point
                    else:
                        color = self.draggingPointColor
                    
                    # Draw Point at current mouse position when Dragging
                    if sE:
                        pygame.draw.circle(self.screen, color, self.mouse_position, self.pointRadius, 0)

                    # Do not draw Point Data if drawing Parabola
                    # AKA: Draw Point Data if Dragging Point 1 or Point 2
                    if not s1 or not s2:
                        self.drawMousePositionData()
                # Paint assigned points
                if s3 and not self.isDragging:
                    self.drawPositionData(self.point3)                
                if s2:
                    self.drawPositionData(self.point2)
                if s1:
                    self.drawPositionData(self.point1)
                if self.isDragging and sE:
                    self.drawPositionData(self.mouse_position)

                # Paint assigned points
                if s1:
                    pygame.draw.circle(self.screen, self.point1Color, self.point1, self.pointRadius, 0)
                if s2:
                    pygame.draw.circle(self.screen, self.point2Color, self.point2, self.pointRadius, 0)
                if s3 and not self.isDragging:
                    pygame.draw.circle(self.screen, self.point3Color, self.point3, self.pointRadius, 0)
                self.drawFPS()
            pygame.display.update()
        pygame.quit()
        return

    def updateMousePosition(self,event):
        self.mouse_position = event.pos
    def decreaseStepAmount(self):
        
        self.parabolaStepCount -= self.parabolaStepDelta
        if (self.parabolaStepCount < self.parabolaStepMin):
            self.parabolaStepCount = self.parabolaStepMin
        if self.parabola != None:
            self.parabola.change_steps(self.parabolaStepCount)
        self.reCalculate = True
    def increaseStepAmount(self):
        self.parabolaStepCount += self.parabolaStepDelta
        if (self.parabolaStepCount > self.parabolaStepMax):
            self.parabolaStepCount = self.parabolaStepMax
        if self.parabola != None:
            self.parabola.change_steps(self.parabolaStepCount)
        self.reCalculate = True
    def decreaseTickAmount(self):
        self.currentTickDistance -= self.tickAmount
        if (self.currentTickDistance < self.minTickSize):
            self.currentTickDistance = self.minTickSize    
    def increaseTickAmount(self):
        self.currentTickDistance += self.tickAmount
        if (self.currentTickDistance > self.maxTickSize):
            self.currentTickDistance = self.maxTickSize    
    def toggleFPS(self):
        self.showFPS = not self.showFPS
    def nextErrorMode(self):
        self.errorDisplayMode += 1
        if self.errorDisplayMode > 15:
            self.errorDisplayMode = 0
    def toggleStatic(self):
        self.isInfoStatic = not self.isInfoStatic
    def toggleGrid(self):
        self.showGrid = not self.showGrid
    def toggleTicks(self):
        self.showTicks = not self.showTicks
        
    def isLMB(self, button):
        return button == 1
    def isMMB(self, button):
        return button == 2
    def isRMB(self, button):
        return button == 3
    def isMouseWheelUp(self, button):
        return button == 4
    def isMouseWheelDown(self, button):
        return button == 5
    def isBadPoint(self, point):
        return point == self.badPoint
    def isPointOnScreen(self, p):
        if self.isBadPoint(p):
            return False
        return (p[0] >= 0 and p[1] >= 0 and 
                p[0] <= self.width and p[1] <= self.height)

    def drawAxesAndGrid(self, drawPoint):
        if (not self.isPointOnScreen(drawPoint)):
            return
        for j in range(0, self.height):
            if ( (j - drawPoint[1]) % self.currentTickDistance == 0):
                if self.showGrid:
                    pygame.draw.line(self.screen, self.gridColor, (0, j), (self.width, j), 1)
                if self.showTicks:
                    pygame.draw.line(self.screen, self.tickColor, (drawPoint[0]-self.tickDrawSize/2, j), (drawPoint[0]+self.tickDrawSize/2,  j), 1)
        for i in range(0, self.width):
            if ( (i - drawPoint[0]) % self.currentTickDistance == 0):
                if self.showGrid:
                    pygame.draw.line(self.screen, self.gridColor, (i, 0), (i, self.height), 1)
                if self.showTicks:
                    pygame.draw.line(self.screen, self.tickColor, (i, drawPoint[1]-self.tickDrawSize/2), (i, drawPoint[1]+self.tickDrawSize/2), 1)
        pygame.draw.line(self.screen, self.axesColor, (0     , drawPoint[1]), (self.width,  drawPoint[1]), 1)
        pygame.draw.line(self.screen, self.axesColor, (drawPoint[0], 0     ), (drawPoint[0], self.height), 1)
        return

    def drawMousePositionData(self):
        baseDrawPoint = (self.mouse_position[0]+self.staticOffsetX,self.mouse_position[1]+self.staticOffsetY)
        myfontS = pygame.font.SysFont('monospace', self.infoFontSize)
        Print1 = '{0}'.format(Point.fromtuple(self.mouse_position))
        ts1 = myfontS.render(Print1, False, self.mousePositionTextColor, self.mousePositionBackColor)
        self.screen.blit(ts1,baseDrawPoint)
        return
    
    def drawPositionData(self, point):
        baseDrawPoint = (point[0]+self.staticOffsetX,point[1]+self.staticOffsetY)
        myfontS = pygame.font.SysFont('monospace', self.infoFontSize)
        Print1 = '{0}'.format(Point.fromtuple(point))
        ts1 = myfontS.render(Print1, False, self.mousePositionTextColor, self.mousePositionBackColor)
        self.screen.blit(ts1,baseDrawPoint)
        return
    def drawParabola(self):
        if self.parabola == None:
            return
        p = self.parabola
        if (self.parabolaCounter > 1):
            p2 = Parabola(p.known_points[0].astuple(), (p.known_points[1].x, p.known_points[1].y - 75), p.known_points[2].astuple(), p.steps)
            rect = pygame.draw.lines(self.screen, self.parabolaColor, False, p2.get_list(), 1)
            if self.drawBoundingBox:
                pygame.draw.rect(self.screen, Colors.RED, rect, 1)
        if (self.parabolaCounter > 2):
            p2 = Parabola(p.known_points[0].astuple(), (p.known_points[1].x, p.known_points[1].y + 75), p.known_points[2].astuple(), p.steps)
            rect = pygame.draw.lines(self.screen, self.parabolaColor, False, p2.get_list(), 1)
            if self.drawBoundingBox:
                pygame.draw.rect(self.screen, Colors.RED, rect, 1)
            
        #rect = pygame.draw.aalines(self.screen, self.parabolaColor, False, parabola.get_list(), 0)
        rect = pygame.draw.lines(self.screen, self.parabolaColor, False, self.parabola.get_list(), 1)
        if self.drawBoundingBox:
            pygame.draw.rect(self.screen, Colors.RED, rect, 1)
        
        return
        
    def drawParabolaData(self):
        if self.parabola == None:
            return
            
        angle = self.parabola.degrees

        # Cheap abs(angle)
        if angle < 0:
            angle = -angle
            
        # Y is inverted in Game Graphics
        slope = -self.parabola.slope
        
        if self.isInfoStatic:
            # Stationary at the "origin" of the axes
            baseDrawPoint = (self.point1[0]+self.staticOffsetX,self.point1[1]+self.staticOffsetY)
        else:
            # Dynamically follows the dragging point when being dragged
            # Otherwise, stationary at the last point dropped
            if self.isDragging:
                baseDrawPoint = (self.mouse_position[0]+self.dynamicOffsetX,self.mouse_position[1]+self.dynamicOffsetY)
            else:
                baseDrawPoint = (self.point3[0]+self.dynamicOffsetX,self.point3[1]+self.dynamicOffsetY)
            
        myfontS = pygame.font.SysFont('monospace', self.infoFontSize)
        Print1 = self.parabola.quadratic
        Print2 = 'ANGLE {0:.2f} SLOPE {1:.2f}'.format(angle, slope)
        Print3 = '{0} {1} {2}'.format(self.parabola.known_points[0], self.parabola.known_points[1], self.parabola.known_points[2])
        
        ts1 = myfontS.render(Print1, False, self.parabolaDataTextColor, self.parabolaDataBackColor)
        ts2 = myfontS.render(Print2, False, self.parabolaDataTextColor, self.parabolaDataBackColor)
        ts3 = myfontS.render(Print3, False, self.parabolaDataTextColor, self.parabolaDataBackColor)
        
        self.screen.blit(ts1, (baseDrawPoint[0], baseDrawPoint[1] + ts1.get_height() + self.infoPadding))
        self.screen.blit(ts2, (baseDrawPoint[0], baseDrawPoint[1] + ts1.get_height()*2 + self.infoPadding*2))
        self.screen.blit(ts3, (baseDrawPoint[0], baseDrawPoint[1] + ts1.get_height()*3 + self.infoPadding*3))
        #self.screen.blit(ts3, (baseDrawPoint[0], baseDrawPoint[1] + ts1.get_height() + self.infoPadding + ts2.get_height() + self.infoPadding))
        return

    def getValueFromBits(self, bits, ts1):
        startx = self.errorPoint[0]
        starty = self.errorPoint[1]
        
        box_width = ts1.get_width()
        box_height = ts1.get_height()
        
        i = bits
        
        if i & self.BIT_CENTER_ON_X:
            startx = (self.width - box_width) / 2
            
        if i & self.BIT_CENTER_ON_Y:
            starty = (self.height - box_height) / 2
            
        box_start_x = startx
        box_start_y = starty

        if i & self.BIT_WIDE_BG:
            box_start_x = 0
            box_width = self.width
            
        if i & self.BIT_TALL_BG:
            box_start_y = 0
            box_height = self.height
            
        return (startx, starty, box_start_x, box_start_y, box_width, box_height)
    
    def drawErrorData(self, e):
        myfontS = pygame.font.SysFont('monospace', self.errorFontSize)
        Print1 = ' {0} '.format(e)
        ts1 = myfontS.render(Print1, False, self.errorTextColor)

        startx, starty, box_start_x, box_start_y, box_width, box_height = self.getValueFromBits(self.errorDisplayMode, ts1)
        if self.showSteps:
            box_start_y += ts1.get_height()
            starty += ts1.get_height()
        pygame.draw.rect(self.screen, self.errorBackColor, (box_start_x, box_start_y, box_width, box_height))
        self.screen.blit(ts1,(startx, starty))
        return
        
    def drawFPS(self):
        myfontS = pygame.font.SysFont('monospace', self.errorFontSize) 
        #PrintE = 'E:{0:3d}'.format(self.errorDisplayMode)
        #tsE = myfontS.render(PrintF, False, self.errorTextColor)
        if self.showSteps:
            PrintS = 'Steps:{0:4d}'.format(self.parabolaStepCount)
            tsS = myfontS.render(PrintS, False, self.errorTextColor)
            startx, starty, box_start_x, box_start_y, box_width, box_height = self.getValueFromBits(self.fpsDisplayMode, tsS)
            pygame.draw.rect(self.screen, self.errorBackColor, (box_start_x, box_start_y, box_width, box_height))
            self.screen.blit(tsS,(startx, starty))
        if self.showFPS:
            PrintF = 'FPS:{0:7.2f}'.format(self.Clock.get_fps())
            tsF = myfontS.render(PrintF, False, self.errorTextColor)
            fpsW = tsF.get_width()
            fpsH = tsF.get_height()
            pygame.draw.rect(self.screen, self.errorBackColor, (self.width-fpsW, self.height-fpsH, fpsW, fpsH))
            self.screen.blit(tsF,(self.width-fpsW,self.height-fpsH))
        return
        
if __name__ == "__main__":
    pMain = ParabolaTest()
    pMain.run()
