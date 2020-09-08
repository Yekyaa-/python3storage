import pygame
import pygame.event
from pygame.locals import *

from python3storage.RandomJunk.ParabolaClass import Parabola
from python3storage.RandomJunk.ParabolaClass import Point


class Colors:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    DARKRED = (127, 0, 0)
    GREEN = (0, 255, 0)
    DARKGREEN = (0, 127, 0)
    BLUE = (0, 0, 255)
    DARKBLUE = (0, 0, 127)
    PURPLE = (255, 0, 255)
    DARKPURPLE = (127, 0, 127)
    LIGHTGRAY = (223, 223, 223)
    TEXTGRAY = (244, 244, 244)
    WHITE = (255, 255, 255)


# noinspection PyTypeChecker
class ParabolaTest:
    def resize(self, event):
        old_surface_saved = self.screen
        self.screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
        self.topLeft = (0, 0)
        self.topRight = (event.w, 0)
        self.bottomLeft = (0, event.h)
        self.bottomRight = (event.w, event.h)
        self.width = event.w
        self.height = event.h
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
        self.font_name = 'couriernew'
        self.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE)
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
        self.infoFontSize = 14
        self.isInfoStatic = True
        self.staticOffsetX = 20
        self.staticOffsetY = 20
        self.dynamicOffsetX = 20
        self.dynamicOffsetY = 20
        self.parabola = None
        self.errorFontSize = 16
        self.errorPoint = (10, 20)

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

        self.topLeft = (0, 0)
        self.topRight = (self.width, 0)
        self.bottomLeft = (0, self.height)
        self.bottomRight = (self.width, self.height)

        self.badPoint = (None, None)
        self.point1 = self.point2 = self.point3 = self.badPoint
        self.axes = self.mouse_position = self.badPoint

    def input_loop(self):
        for event in pygame.event.get():
            # ====================
            # WINDOW EVENTS
            # ====================
            # Window Closed Event
            if event.type == QUIT:
                pygame.quit()
                return False
            # Window Resize Event
            elif event.type == VIDEORESIZE:
                self.resize(event)
            # ====================
            # KEYBOARD EVENTS
            # ====================
            # Key Released Events
            elif event.type == KEYUP:
                # Press ESCAPE to Quit
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return False
                # Press SPACE to Show Grid
                elif event.key == K_LEFT:
                    self.move_left()
                elif event.key == K_SPACE:
                    self.toggle_grid()
                # Press UP ARROW to increase distance between grid lines
                elif event.key == K_UP:
                    self.increase_tick_amount()
                # Press DOWN ARROW to decrease distance between grid lines
                elif event.key == K_DOWN:
                    self.decrease_tick_amount()
                elif event.key == K_b:
                    self.drawBoundingBox = not self.drawBoundingBox
                # Press T to show tick marks on axes
                elif event.key == K_t:
                    self.toggle_ticks()
                # Press P to toggle between static and dynamic positioning of Parabola data
                elif event.key == K_p:
                    self.toggle_static()
                elif event.key == K_f:
                    self.toggle_fps()
                # elif event.key == K_e:
                #    self.next_error_mode()
                elif event.key == K_s:
                    self.showSteps = not self.showSteps
                elif event.key == K_c:
                    self.parabolaCounter += 1
                    if self.parabolaCounter > 3:
                        self.parabolaCounter = 1
            # ====================
            # MOUSE EVENTS
            # ====================
            # While mouse is moving, keep track of mouse position
            elif event.type == MOUSEMOTION:
                self.update_mouse_position(event)
            # MOUSEBUTTONDOWN events    
            elif event.type == MOUSEBUTTONDOWN:
                # Hold LEFT MOUSE BUTTON to Start Dragging
                if self.is_left_mouse_button(event.button):
                    # Turn on Dragging until left mouse RELEASED
                    self.isDragging = True
                    # And update position
                    self.update_mouse_position(event)
                else:
                    # print(event)
                    pass
            # MOUSEBUTTONUP events
            elif event.type == MOUSEBUTTONUP:
                # Release RIGHT MOUSE BUTTON to Clear Screen
                if self.is_right_mouse_button(event.button):
                    # Clear all data
                    self.doReset = True
                # Release LEFT MOUSE BUTTON to Stop Dragging and Assign this Point
                elif self.is_left_mouse_button(event.button):
                    # Save location to new point if necessary or update an old one??? 
                    self.doAssign = True
                    # Update mouse position
                    self.update_mouse_position(event)
                    # Turn off Dragging
                    self.isDragging = False
                elif self.is_mouse_wheel_up(event.button):
                    self.increase_step_amount()
                elif self.is_mouse_wheel_down(event.button):
                    self.decrease_step_amount()
                    # self.decrease_tick_amount()
                elif self.is_middle_mouse_button(event.button):
                    self.toggle_grid()
                else:
                    # print(event)
                    pass
            # ====================
            # UNKNOWN EVENTS
            # ====================
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
        while self.input_loop():
            self.Clock.tick()
            self.screen.fill(self.screenFillColor)
            if self.doReset:
                self.point1 = self.point2 = self.point3 = self.badPoint
                self.doReset = False
            else:
                if self.doAssign:
                    if not self.is_point_on_screen(self.point1):
                        self.point1 = self.mouse_position
                    elif not self.is_point_on_screen(self.point2):
                        self.point2 = self.mouse_position
                    else:
                        self.point3 = self.mouse_position
                    self.doAssign = False

                s1 = self.is_point_on_screen(self.point1)
                s2 = self.is_point_on_screen(self.point2)
                s3 = self.is_point_on_screen(self.point3)
                s_e = self.is_point_on_screen(self.mouse_position)

                if not s1 and s_e and self.isDragging:
                    self.draw_axes_and_grid(self.mouse_position)
                else:
                    self.draw_axes_and_grid(self.point1)

                # Require Points 1 & 2 with either Point 3 set, or currently being placed to draw Parabola
                if s1 and s2:
                    try:
                        if not self.isDragging and s3:
                            if self.parabola is None or self.reCalculate:
                                self.parabola = Parabola(self.point1, self.point2, self.point3, self.parabolaStepCount)
                                self.reCalculate = False
                            self.draw_parabola()
                            self.draw_parabola_data()
                        elif self.isDragging and s_e:
                            self.parabola = Parabola(self.point1, self.point2, self.mouse_position,
                                                     self.parabolaStepCount)
                            self.draw_parabola()
                            self.draw_parabola_data()
                    except ValueError as e:
                        del self.parabola
                        self.parabola = None
                        self.draw_error_data(e)

                # Only Drag one point at a time
                if self.isDragging:
                    # If first point not set, drag it
                    if not s1:
                        pt_color = self.point1Color
                    # If second point not set, drag it
                    elif not s2:
                        pt_color = self.point2Color
                    # If third point not set, drag it
                    elif not s3:
                        pt_color = self.point3Color
                    # All dots assigned, drag "new position" of third point
                    else:
                        pt_color = self.draggingPointColor

                    # Draw Point at current mouse position when Dragging
                    if s_e:
                        pygame.draw.circle(self.screen, pt_color, self.mouse_position, self.pointRadius, 0)

                    # Do not draw Point Data if drawing Parabola
                    # AKA: Draw Point Data if Dragging Point 1 or Point 2
                    if not s1 or not s2:
                        self.draw_mouse_position_data()
                # Paint assigned points
                if s3 and not self.isDragging:
                    self.draw_position_data(self.point3)
                if s2:
                    self.draw_position_data(self.point2)
                if s1:
                    self.draw_position_data(self.point1)
                if self.isDragging and s_e:
                    self.draw_position_data(self.mouse_position)

                # Paint assigned points
                if s1:
                    pygame.draw.circle(self.screen, self.point1Color, self.point1, self.pointRadius, 0)
                if s2:
                    pygame.draw.circle(self.screen, self.point2Color, self.point2, self.pointRadius, 0)
                if s3 and not self.isDragging:
                    pygame.draw.circle(self.screen, self.point3Color, self.point3, self.pointRadius, 0)
                self.draw_fps()
            pygame.display.update()
        pygame.quit()
        return

    def update_mouse_position(self, event):
        self.mouse_position = event.pos

    def decrease_step_amount(self):

        self.parabolaStepCount -= self.parabolaStepDelta
        if self.parabolaStepCount < self.parabolaStepMin:
            self.parabolaStepCount = self.parabolaStepMin
        if self.parabola is not None:
            self.parabola.change_steps(self.parabolaStepCount)
        self.reCalculate = True

    def increase_step_amount(self):
        self.parabolaStepCount += self.parabolaStepDelta
        if self.parabolaStepCount > self.parabolaStepMax:
            self.parabolaStepCount = self.parabolaStepMax
        if self.parabola is not None:
            self.parabola.change_steps(self.parabolaStepCount)
        self.reCalculate = True

    def decrease_tick_amount(self):
        self.currentTickDistance -= self.tickAmount
        if self.currentTickDistance < self.minTickSize:
            self.currentTickDistance = self.minTickSize

    def increase_tick_amount(self):
        self.currentTickDistance += self.tickAmount
        if self.currentTickDistance > self.maxTickSize:
            self.currentTickDistance = self.maxTickSize

    def toggle_fps(self):
        self.showFPS = not self.showFPS

    def next_error_mode(self):
        self.errorDisplayMode += 1
        if self.errorDisplayMode > 15:
            self.errorDisplayMode = 0

    def toggle_static(self):
        self.isInfoStatic = not self.isInfoStatic

    def toggle_grid(self):
        self.showGrid = not self.showGrid

    def toggle_ticks(self):
        self.showTicks = not self.showTicks

    @staticmethod
    def is_left_mouse_button(button):
        return button == 1

    @staticmethod
    def is_middle_mouse_button(button):
        return button == 2

    @staticmethod
    def is_right_mouse_button(button):
        return button == 3

    @staticmethod
    def is_mouse_wheel_up(button):
        return button == 4

    @staticmethod
    def is_mouse_wheel_down(button):
        return button == 5

    def is_bad_point(self, point):
        return point == self.badPoint

    def is_point_on_screen(self, p):
        if self.is_bad_point(p):
            return False
        return 0 <= p[0] <= self.width and 0 <= p[1] <= self.height

    def draw_axes_and_grid(self, draw_point):
        if not self.is_point_on_screen(draw_point):
            return
        for j in range(0, self.height):
            if (j - draw_point[1]) % self.currentTickDistance == 0:
                if self.showGrid:
                    pygame.draw.line(self.screen, self.gridColor, (0, j), (self.width, j))
                if self.showTicks:
                    pygame.draw.line(self.screen, self.tickColor, (int(draw_point[0] - self.tickDrawSize / 2), j),
                                     (int(draw_point[0] + self.tickDrawSize / 2), j))
        for i in range(0, self.width):
            if (i - draw_point[0]) % self.currentTickDistance == 0:
                if self.showGrid:
                    pygame.draw.line(self.screen, self.gridColor, (i, 0), (i, self.height))
                if self.showTicks:
                    pygame.draw.line(self.screen, self.tickColor, (i, int(draw_point[1] - self.tickDrawSize / 2)),
                                     (i, int(draw_point[1] + self.tickDrawSize / 2)))
        pygame.draw.line(self.screen, self.axesColor, (0, draw_point[1]), (self.width, draw_point[1]))
        pygame.draw.line(self.screen, self.axesColor, (draw_point[0], 0), (draw_point[0], self.height))
        return

    def draw_mouse_position_data(self):
        if self.mouse_position != self.badPoint and self.mouse_position[0] is not None \
                and self.mouse_position[1] is not None:
            base_draw_point = (self.mouse_position[0] + self.staticOffsetX, self.mouse_position[1] + self.staticOffsetY)
            my_sys_font = pygame.font.SysFont(self.font_name, self.infoFontSize)
            line = '{0}'.format(Point.from_(self.mouse_position))
            ts1 = my_sys_font.render(line, False, self.mousePositionTextColor, self.mousePositionBackColor)
            self.screen.blit(ts1, base_draw_point)
        return

    def draw_position_data(self, point):
        if point != self.badPoint:
            base_draw_point = (point[0] + self.staticOffsetX, point[1] + self.staticOffsetY)
            my_sys_font = pygame.font.SysFont(self.font_name, self.infoFontSize)
            print1 = '{0}'.format(Point.from_(point))

            ts1 = my_sys_font.render(print1, False, self.mousePositionTextColor, self.mousePositionBackColor)
            self.screen.blit(ts1, base_draw_point)
        return

    # noinspection SpellCheckingInspection
    def draw_parabola(self):
        if self.parabola is None:
            return
        p = self.parabola

        if self.parabolaCounter > 1:
            p2 = Parabola(p.known_points[0].as_tuple(), (p.known_points[1].x, p.known_points[1].y - 75),
                          p.known_points[2].as_tuple(), p.steps)
            rect = pygame.draw.lines(self.screen, self.parabolaColor, False, p2.get_int_list(), 1)
            if self.drawBoundingBox:
                pygame.draw.rect(self.screen, Colors.RED, rect, 1)
        if self.parabolaCounter > 2:
            p2 = Parabola(p.known_points[0].as_tuple(), (p.known_points[1].x, p.known_points[1].y + 75),
                          p.known_points[2].as_tuple(), p.steps)
            rect = pygame.draw.lines(self.screen, self.parabolaColor, False, p2.get_int_list(), 1)
            if self.drawBoundingBox:
                pygame.draw.rect(self.screen, Colors.RED, rect, 1)

        # rect = pygame.draw.aalines(self.screen, self.parabolaColor, False, parabola.get_list(), 0)
        int_list = self.parabola.get_int_list()
        rect = pygame.draw.lines(self.screen, self.parabolaColor, False, int_list)

        if self.drawBoundingBox:
            pygame.draw.rect(self.screen, Colors.RED, rect, 1)

        return

    def draw_parabola_data(self):
        if self.parabola is None:
            return

        angle = self.parabola.degrees

        # Cheap abs(angle)
        if angle < 0:
            angle = -angle

        # Y is inverted in Game Graphics
        slope = -self.parabola.slope

        if self.isInfoStatic:
            # Stationary at the "origin" of the axes
            base_draw_point = (self.point1[0] + self.staticOffsetX, self.point1[1] + self.staticOffsetY)
        else:
            # Dynamically follows the dragging point when being dragged
            # Otherwise, stationary at the last point dropped
            if self.isDragging:
                base_draw_point = (
                    self.mouse_position[0] + self.dynamicOffsetX, self.mouse_position[1] + self.dynamicOffsetY)
            else:
                base_draw_point = (self.point3[0] + self.dynamicOffsetX, self.point3[1] + self.dynamicOffsetY)

        my_sys_font = pygame.font.SysFont(self.font_name, self.infoFontSize)

        print1 = self.parabola.quadratic
        print2 = 'ANGLE {0:.2f} SLOPE {1:.2f}'.format(angle, slope)
        print3 = '{0} {1} {2}'.format(self.parabola.known_points[0], self.parabola.known_points[1],
                                            self.parabola.known_points[2])
        ts1 = my_sys_font.render(print1, False, self.parabolaDataTextColor, self.parabolaDataBackColor)
        ts2 = my_sys_font.render(print2, False, self.parabolaDataTextColor, self.parabolaDataBackColor)
        ts3 = my_sys_font.render(print3, False, self.parabolaDataTextColor, self.parabolaDataBackColor)

        self.screen.blit(ts1, (base_draw_point[0], base_draw_point[1] + ts1.get_height() + self.infoPadding))
        self.screen.blit(ts2, (base_draw_point[0], base_draw_point[1] + ts1.get_height() * 2 + self.infoPadding * 2))
        self.screen.blit(ts3, (base_draw_point[0], base_draw_point[1] + ts1.get_height() * 3 + self.infoPadding * 3))
        # self.screen.blit(ts3, (base_draw_point[0], base_draw_point[1] + ts1.get_height()
        # + self.infoPadding + ts2.get_height() + self.infoPadding))
        return

    def get_value_from_bits(self, bits, ts1):
        start_x = self.errorPoint[0]
        start_y = self.errorPoint[1]

        box_width = ts1.get_width()
        box_height = ts1.get_height()

        i = bits

        if i & self.BIT_CENTER_ON_X:
            start_x = (self.width - box_width) / 2

        if i & self.BIT_CENTER_ON_Y:
            start_y = (self.height - box_height) / 2

        box_start_x = start_x
        box_start_y = start_y

        if i & self.BIT_WIDE_BG:
            box_start_x = 0
            box_width = self.width

        if i & self.BIT_TALL_BG:
            box_start_y = 0
            box_height = self.height

        return start_x, start_y, box_start_x, box_start_y, box_width, box_height

    def draw_error_data(self, e):
        my_sys_font = pygame.font.SysFont(self.font_name, self.errorFontSize)
        print1 = ' {0} '.format(e)
        ts1 = my_sys_font.render(print1, False, self.errorTextColor)

        start_x, start_y, box_start_x, box_start_y, box_width, box_height = self.get_value_from_bits(
            self.errorDisplayMode,
            ts1)
        if self.showSteps:
            box_start_y += ts1.get_height()
            start_y += ts1.get_height()
        pygame.draw.rect(self.screen, self.errorBackColor, (int(box_start_x), int(box_start_y), box_width, box_height))
        self.screen.blit(ts1, (int(start_x), int(start_y)))
        return

    def draw_fps(self):
        my_sys_font = pygame.font.SysFont(self.font_name, self.errorFontSize)
        # PrintE = 'E:{0:3d}'.format(self.errorDisplayMode)
        # tsE = my_sys_font.render(print_f, False, self.errorTextColor)
        if self.showSteps:
            print_s = 'Steps:{0:4d}'.format(self.parabolaStepCount)
            ts_s = my_sys_font.render(print_s, False, self.errorTextColor)
            start_x, start_y, box_start_x, box_start_y, box_width, box_height = self.get_value_from_bits(
                self.fpsDisplayMode,
                ts_s)
            pygame.draw.rect(self.screen, self.errorBackColor, (box_start_x, box_start_y, box_width, box_height))
            self.screen.blit(ts_s, (int(start_x), int(start_y)))
        if self.showFPS:
            print_f = 'FPS:{0:7.2f}'.format(self.Clock.get_fps())
            ts_f = my_sys_font.render(print_f, False, self.errorTextColor)
            fps_w = ts_f.get_width()
            fps_h = ts_f.get_height()
            pygame.draw.rect(self.screen, self.errorBackColor, (self.width - fps_w, self.height - fps_h, fps_w, fps_h))
            self.screen.blit(ts_f, (self.width - fps_w, self.height - fps_h))
        return

    def move_left(self):
        pass


if __name__ == "__main__":
    pMain = ParabolaTest()
    pMain.run()
