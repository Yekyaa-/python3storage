import math
import random
import time

import pygame
import pygame.event
from pygame.locals import *

from python3storage.Classes.BoxDraw import BoxDrawer
from python3storage.Classes.Point import Point
from python3storage.Classes.Shape import Shape


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


# noinspection PyTypeChecker,PyMethodMayBeStatic
class TheWindow:
    def __init__(self):
        self.delta_between_origins = 0
        self.shape = None
        self.selected_side_count = 2

        self.hovering = None
        self.print_data = {'y_line_counter': 0, 'x_line_counter': 0, 'mult_count': 0, 'timer': 0, 'special_menu': ''}
        self.debug_menu = None

        """__init__ -- Establishes TheWindow and starts necessary processes """
        self.spare = 3000000
        self.largest_polygon = 25
        pygame.init()
        pygame.font.init()
        self.mouseDownAt = None
        self.mouseUpAt = None
        self.mouse_click_start = None
        self.mouse_click_end = None
        self.defaultPolygonRadius = 20

        self.currentMouseData = {}

        self.Clock = pygame.time.Clock()
        self.width = 700
        self.height = 650

        self.origin = Point(self.width // 2, self.height // 2)
        self.axes_origin = self.origin
        self.zoom_location = self.origin

        self.polygon_list = []
        self.point_list = []
        self.scale = 1.0
        self.rotation = 0.0

        self.infoPadding = 1
        self.isInfoStatic = True
        self.font_name = 'couriernew'
        self.font_name_fixed = 'consolas'
        self.infoFontSize = 14
        self.sys_font = pygame.font.SysFont(self.font_name, self.infoFontSize)
        self.sys_font_fixed = pygame.font.SysFont(self.font_name_fixed, self.infoFontSize + 3)
        t_font_render = self.sys_font_fixed.render(' ', False, Colors.WHITE, Colors.BLACK)
        self.font_height = t_font_render.get_height()
        # print(self.infoFontSize, self.font_height)
        del t_font_render

        self.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE)
        pygame.display.set_caption('Axes Sandbox')

        self.BIT_CENTER_HORIZONTALLY = 1
        """ BIT_CENTER_HORIZONTALLY means text is centered horizontally """
        self.BIT_CENTER_VERTICALLY = 2
        """ BIT_CENTER_VERTICALLY means text is centered vertically """
        self.BIT_BG_STRETCH_HORIZONTALLY = 4
        """ BIT_BG_STRETCH_HORIZONTALLY means background is stretched horizontally """
        self.BIT_BG_STRETCH_VERTICALLY = 8
        """ BIT_BG_STRETCH_VERTICALLY means background is stretched vertically """

        self.errorDisplayMode = self.BIT_CENTER_HORIZONTALLY
        self.fpsDisplayMode = self.BIT_CENTER_HORIZONTALLY | self.BIT_BG_STRETCH_HORIZONTALLY
        self.showSteps = True
        self.showFPS = True
        self.reCalculate = False
        self.screenFillColor = Colors.WHITE
        self.errorBackColor = Colors.BLACK
        self.errorTextColor = Colors.WHITE

        self.mousePositionTextColor = Colors.BLACK
        self.mousePositionBackColor = Colors.TEXTGRAY
        self.axesColor = Colors.BLACK

        self.point1Color = Colors.DARKGREEN
        self.point2Color = Colors.DARKBLUE
        self.point3Color = Colors.DARKRED
        self.draggingPointColor = Colors.PURPLE
        self.gridColor = Colors.LIGHTGRAY
        self.tickColor = Colors.BLACK
        self.staticOffsetX = 20
        self.staticOffsetY = 20
        self.dynamicOffsetX = 20
        self.dynamicOffsetY = 20

        self.errorFontSize = 16
        self.errorPoint = (10, 20)

        self.isDragging = False
        self.isHolding = False

        self.show_debug_menu = False
        self.showGrid = True
        self.showTicks = True
        self.tickDrawSize = 6
        self.defaultTickDistance = 10
        self.currentTickDistance = 10
        self.tickAmount = .1
        self.minTickSize = .1
        self.maxTickSize = 750

        self.pointRadius = 5

        self.topLeft = (0, 0)
        self.topRight = (self.width, 0)
        self.bottomLeft = (0, self.height)
        self.bottomRight = (self.width, self.height)

        self.point1 = self.point2 = self.point3 = None
        self.axes = None
        self.mouse_position = pygame.mouse.get_pos()
        self.dragStart = None
        self.mouse_do_drag = self.handle_do_drag
        self.mouse_drag_end = self.handle_drag_end
        self.mouse_up = self.handle_mouse_up
        self.mouse_down = self.handle_mouse_down
        self.mouse_move = self.handle_mouse_move
        self.draw_axes_and_grid = self.draw_axes_and_grid_new
        if len(self.point_list) < 2:
            self.point_list.clear()
            self.point_list.append(Point(0, 0))
            self.point_list.append(Point(10, 10))
            self.point_list.append(Point(10, 0))

    def reset_canvas(self):
        self.mouse_position = pygame.mouse.get_pos()
        self.zoom_location = self.origin
        self.show_debug_menu = False
        self.showGrid = True
        self.showTicks = True
        self.tickDrawSize = 6
        self.defaultTickDistance = 10
        self.currentTickDistance = 10
        self.tickAmount = .1
        self.minTickSize = .1
        self.maxTickSize = 750
        self.axes_origin = self.origin
        self.polygon_list = []
        self.point_list = []
        self.scale = 1.0
        if len(self.point_list) < 2:
            self.point_list.clear()
            self.point_list.append(Point(0, 0))
            self.point_list.append(Point(10, 10))
            self.point_list.append(Point(10, 0))
        # self.__init__()

    def draw_canvas(self):
        self.screen.fill(self.screenFillColor)

        #     if len(self.point_list):
        #         self.point_list.pop(0)
        #         self.point_list.insert(0, self.mouse_position)
        # elif len(self.point_list):
        #     self.origin = self.point_list[0]
        # this_data = f'Drag: {str(self.isDragging):>6}  Hold: {str(self.isHolding):>6}  A:{self.axes_origin}'
        y_line = self.print_data['y_line_counter']
        x_line = self.print_data['x_line_counter']
        # this_data = f'V_LINE:{x_line} H_LINE:{y_line}'
        self.draw_axes_and_grid()
        self.draw_points()
        self.draw_polygons()
        self.draw_timer_data()
        self.draw_fps_data()
        self.draw_mouse_position_data()

        if self.show_debug_menu:
            self.debug_menu = self.draw_debug_menu(selected=self.hovering)
        pygame.display.update()

    def draw_axes_and_grid_new(self):
        # point of origin (where axes are drawn at)
        ap = self.axes_origin

        # Translate edges to figure out if I need lines or not.
        top_left = self.translate_to_world((0, 0), None)
        bottom_right = self.translate_to_world((self.width, self.height), None)
        tx, ty = top_left
        start_x, start_y = math.ceil(tx), math.ceil(ty)
        bx, by = bottom_right
        end_x, end_y = math.floor(bx), math.floor(by)
        if self.currentTickDistance >= 10:
            offset = 0
        elif self.currentTickDistance >= 5:
            offset = 1
        elif self.currentTickDistance >= 2:
            offset = 2

        step_amount = 1
        ok_to_draw = True
        if self.currentTickDistance < 3:
            step_amount = 2
            ok_to_draw = False

        self.print_data['x_line_counter'] = 0
        if self.showGrid and end_x >= start_x:
            for x in range(start_x, end_x + 1, step_amount):
                p = self.translate_to_screen((x, 0), self.axes_origin)
                assert type(p[0]) is int, f'{p[0]}'
                if self.showGrid and ok_to_draw:
                    self.print_data['x_line_counter'] += 1
                    pygame.draw.line(self.screen, self.gridColor, (p[0], 0), (p[0], self.height))
                if self.showTicks and ok_to_draw:
                    tick_top = int(ap[1] - self.tickDrawSize / 2 + offset)
                    tick_bottom = int(ap[1] + self.tickDrawSize / 2 - offset)
                    assert type(tick_top) is int, f'{tick_top}'
                    assert type(tick_bottom) is int, f'{tick_bottom}'
                    pygame.draw.line(self.screen, self.tickColor, (p[0], tick_top), (p[0], tick_bottom))

        self.print_data['y_line_counter'] = 0

        if self.showGrid and end_y <= start_y:
            for y in range(end_y, start_y, step_amount):
                p = self.translate_to_screen((0, y), self.axes_origin)
                assert type(p[1]) is int, f'{p[1]}'
                if self.showGrid and ok_to_draw:
                    self.print_data['y_line_counter'] += 1
                    pygame.draw.line(self.screen, self.gridColor, (0, p[1]), (self.width, p[1]))
                if self.showTicks and ok_to_draw:
                    tick_left = int(ap[0] - self.tickDrawSize / 2 + offset)
                    tick_right = int(ap[0] + self.tickDrawSize / 2 - offset)
                    assert type(tick_left) is int, f'{tick_left}'
                    assert type(tick_right) is int, f'{tick_right}'
                    pygame.draw.line(self.screen, self.tickColor, (tick_left, p[1]),
                                     (tick_right, p[1]))

        pygame.draw.line(self.screen, self.axesColor, (0, self.axes_origin[1]), (self.width, self.axes_origin[1]))
        pygame.draw.line(self.screen, self.axesColor, (self.axes_origin[0], 0), (self.axes_origin[0], self.height))

    def is_event_in_debug_menu(self, pos):
        rect_lst = self.debug_menu
        if rect_lst:
            # print(len(rect_lst), pos, rect_lst)
            for rect in self.debug_menu:
                # print(f'{pygame.Surface}')
                # print(f'{pygame.Surface.get_bounding_rect()=}')
                # print(f'{rect=}')
                # print(f'{rect.get_rect()=}')
                # # a = pygame.Surface.get_size()
                # print(f'{rect.get_size()=}')
                # print(f'{rect.get_offset()=}')
                # # pygame.Surface.get_abs_parent()
                # print(f'{rect.get_bounding_rect()=}')
                if rect[0] <= pos[0] <= rect[2] and rect[1] <= pos[1] <= rect[3]:
                    # print(f'{pos=} is HO{rect=}')
                    # print('is_event_in_debug_menu:     Hovering Over Menu')
                    return rect

        # if event.pos in [rect_lst[0].]
        # print('is_event_in_debug_menu: NOT Hovering Over Menu')
        self.hovering = None
        return None

    def draw_debug_menu(self, selected=None):
        # self.print_data['special_menu']
        rect = []
        line_lst = self.print_data['special_menu'].splitlines(keepends=False)

        point = Point(100, 0)
        # rect.append(point)
        for line in line_lst:
            base_draw_point = (point[0], point[1])

            ts1 = self.sys_font_fixed.render(line, False, Colors.WHITE, Colors.BLACK)

            bdp = base_draw_point
            rct = ts1.get_size()

            new_rect = (bdp[0], bdp[1], bdp[0] + rct[0], bdp[1] + rct[1])

            if new_rect == selected:
                self.hovering = selected

                ts1 = self.sys_font_fixed.render(line, False, Colors.WHITE, Colors.BLUE)

            # print(f'{new_rect} == {select}? {new_rect == select}')

            # print(f'Added {new_rect} to list')
            rect.append(new_rect)
            point[1] = point[1] + self.font_height - 1
            event_pos = selected
            self.screen.blit(ts1, base_draw_point)

        # rect.append(point + (0, self.font_height - 1))
        return rect

    def draw_points(self, point=None):
        if point is None:
            point = self.mouse_position
            # .axes_origin

        prev_point = None
        point_counter = 0

        for p in self.point_list:
            f = self.translate_to_screen(p, self.axes_origin)
            p_color = self.get_dot_color(f)
            self.draw_position_data(p, f)

            if f is float:
                print('f is float', f)
            elif type(f[0]) is float or type(f[1]) is float:
                print('f is float 2:', f[0], f[1])

            pygame.draw.circle(self.screen, p_color, f, self.pointRadius, 0)

            if prev_point is not None:
                pygame.draw.line(self.screen, (0, 0, 0), prev_point, f)
            point_counter += 1
            prev_point = f
        if len(self.point_list) >= 3:
            a = self.translate_to_screen(self.point_list[0], self.axes_origin)
            pygame.draw.line(self.screen, (0, 0, 0), f, a)
            # if point_counter % 4:
            #     prev_point = f
            # else:
            #     prev_point = None

    def draw_polygons(self):
        # region Draw the "select a polygon" hovering polygon
        if self.shape and not self.isHolding:
            # print(f'{self.selected_side_count=}')
            p = Shape(self.selected_side_count,
                      centroid=self.translate_to_world(self.mouse_position, self.mouse_position),
                      rot_angle=(self.shape.rot_angle - 0.25) % 360,
                      rot_point=self.translate_to_world(self.mouse_position, self.mouse_position),
                      radius=self.shape.radius)
            self.shape = p
            p = self.shape
            p_color = Colors.RED  # Colors.TEXTGRAY
            p_l = tuple(p.point_list_int_scaled(self.scale))
            # print(f'draw_polygons:{p_l=}')
            new_list = [(point_v, self.translate_to_screen(point_v, self.mouse_position)) for point_v in p]
            # print(f'{new_list=}')
            p_l = [i[1] for i in new_list]
            # print(f'{p_l=}')
            pygame.draw.polygon(self.screen, p_color, p_l, 2)
        # endregion

        # for each polygon in the list
        for p in self.polygon_list:
            # Get a list of tuple points, under the current scaling system
            p_l = tuple(p.point_list_int_scaled(self.scale))
            t = Shape(p)
            p_color = Colors.BLACK
            c = p.get_centroid()
            z = self.translate_to_screen(c).int()

            new_list = [(point_v, self.translate_to_screen(point_v)) for point_v in p]
            for i in new_list:
                assert type(i[1][0]) is int and type(i[1][1]) is int, f'{i[1]=} is not int!'
                self.draw_position_data(i[0], i[1])

            p_l = [i[1] for i in new_list]

            pygame.draw.polygon(self.screen, (0, 0, 0), p_l, 2)
            pygame.draw.circle(self.screen, Colors.GREEN, z, self.pointRadius, 0)
            self.draw_position_data(c, z)

    def draw_position_data(self, point=None, f=None):
        line = ''

        if point is not None:
            line += f'{Point(point).round(3)} '

        if f is None:
            f = self.translate_to_screen(point, self.axes_origin)
        base_draw_point = Point(f[0] + self.staticOffsetX, f[1] + self.staticOffsetY).int()
        line += f'{f.int()}'
        ts1 = self.sys_font.render(line, False, self.mousePositionTextColor, self.mousePositionBackColor)
        self.screen.blit(ts1, base_draw_point)

    def draw_mouse_position_data(self):
        """	
        Draws mouse cursor and reticle, if not holding left mouse button.	
        Returns:	
        """
        if not self.isHolding and pygame.mouse.get_focused() and self.mouse_position is not None:
            # Random color based on mouse position
            p_color = self.get_dot_color(self.mouse_position)
            # convert mouse_position to world coordinates
            z = self.translate_to_world(self.mouse_position)

            mpx = self.mouse_position[0]
            mpy = self.mouse_position[1]
            line = f'{Point(z):6.3f} {mpx, mpy}'
            # Calculate the point for text (20, 20) to the left/bottom
            base_draw_point = (mpx + self.staticOffsetX, mpy + self.staticOffsetY)

            # Create the text label
            ts1 = self.sys_font.render(line, False, self.mousePositionTextColor, self.mousePositionBackColor)

            # Blit it to the point
            self.screen.blit(ts1, base_draw_point)

            # Draw reticle
            pygame.draw.line(self.screen, p_color, (mpx - 10, mpy), (mpx + 10, mpy), 3)
            pygame.draw.line(self.screen, p_color, (mpx, mpy - 10), (mpx, mpy + 10), 3)

    def draw_timer_data(self):
        """	
        Draw timer data.	
        Returns:	
        """
        timer_value = self.print_data['timer']
        timer = f'{timer_value:7.2f}ms'

        ts1 = self.sys_font.render(timer, False, self.errorTextColor)

        start_x, start_y, box_start_x, box_start_y, box_width, box_height = self.get_value_from_bits(
            self.errorDisplayMode,
            ts1)
        if self.showSteps:
            box_start_y += ts1.get_height()
            start_y += ts1.get_height()
        pygame.draw.rect(self.screen, self.errorBackColor, (int(box_start_x), int(box_start_y), box_width, box_height))
        self.screen.blit(ts1, (int(start_x), int(start_y)))
        return

    def draw_error_data(self, e):
        print1 = ' {0} '.format(e)
        ts1 = self.sys_font.render(print1, False, self.errorTextColor)

        start_x, start_y, box_start_x, box_start_y, box_width, box_height = self.get_value_from_bits(
            self.errorDisplayMode,
            ts1)
        if self.showSteps:
            box_start_y += ts1.get_height()
            start_y += ts1.get_height()
        pygame.draw.rect(self.screen, self.errorBackColor, (int(box_start_x), int(box_start_y), box_width, box_height))
        self.screen.blit(ts1, (int(start_x), int(start_y)))
        return

    def draw_fps_data(self):
        # PrintE = 'E:{0:3d}'.format(self.errorDisplayMode)
        # tsE = my_sys_font.render(print_f, False, self.errorTextColor)
        if self.showFPS:
            z_percent = self.currentTickDistance * 100.0 / self.defaultTickDistance
            fps_data = f'CT:{self.currentTickDistance} Z:{z_percent:5.0f}% T:{self.tickAmount:7.2f} '
            fps_data += f'P: {self.largest_polygon:03} FPS:{self.Clock.get_fps():7.2f}'

            ts_f = self.sys_font.render(fps_data, False, self.errorTextColor)
            fps_w = ts_f.get_width()
            fps_h = ts_f.get_height()
            pygame.draw.rect(self.screen, self.errorBackColor, (self.width - fps_w, self.height - fps_h, fps_w, fps_h))
            self.screen.blit(ts_f, (self.width - fps_w, self.height - fps_h))
        return

    def handle_mouse_move(self, event):
        if self.show_debug_menu and (result := self.is_event_in_debug_menu(event.pos)):
            # print(f'{result=}')
            self.debug_menu = self.draw_debug_menu(selected=result)
        elif event.buttons[0]:
            self.isDragging = True
            self.isHolding = True
            self.mouse_do_drag(event)
        else:
            self.isHolding = False

    def handle_mouse_up(self, event):
        mods = pygame.key.get_mods()
        # print('mouse_up:' + str(event.pos) + ' ' + str(event.button))
        # Release RIGHT MOUSE BUTTON to Clear Screen
        if event.button == BUTTON_RIGHT:
            mods = pygame.key.get_mods()
            # Clear all data
            if mods & KMOD_CTRL and mods & KMOD_SHIFT:
                self.reset_canvas()
            elif mods & KMOD_SHIFT:
                self.polygon_list.clear()
            elif mods & KMOD_CTRL:
                self.point_list.clear()
            elif mods & KMOD_ALT:
                if len(self.polygon_list) > 0:
                    del self.polygon_list[-1]
            # elif len(self.point_list) > 0 and len(self.polygon_list) >= 0:
            #     del self.point_list[-1]
            # elif len(self.point_list) == 0 and len(self.polygon_list) > 0:
            #     del self.polygon_list[-1]

        # Release LEFT MOUSE BUTTON to Stop Dragging and Assign this Point
        elif event.button == BUTTON_LEFT:
            if mods & KMOD_CTRL:
                if self.shape:
                    self.polygon_list.append(
                        self.shape.translate(self.translate_to_world(self.mouse_position, self.axes_origin)))
                self.shape = None
            else:
                # Mouse_Up doesn't happen on Drag_Release
                # Save location to new point if necessary or update an old one???
                self.assign(event.pos)
                # Update mouse position
                self.update_mouse_position(event)
                # Turn off Dragging

    def handle_mouse_down(self, event):
        # print('mouse_down:' + str(event.pos) + ' ' + str(event.button))
        handled = False
        self.mouse_click_start = (pygame.time.get_ticks(), event.button)

        # Hold LEFT MOUSE BUTTON to Start Dragging
        if event.button == BUTTON_LEFT:
            # Turn on Holding until left mouse RELEASED
            self.isHolding = True
            handled = True
        # else:
        #     print(event)
        #
        return handled

    def handle_click(self, event):
        result = False

        return result

    def map_all_polys(self, func=None):
        if func is None:
            return

        for poly in self.polygon_list:
            # o = poly.get_origin()
            # f = func(o)
            # print(f'MAP_ALL:ORIGIN:{o} -> {f}')
            poly.set_centroid(func(poly.get_centroid()))

    def update_all_polys(self, loc=None):
        if loc is None:
            loc = self.axes_origin

        for poly in self.polygon_list:
            poly.set_centroid(Shape.fix_origin(poly))

    def handle_do_drag(self, event):
        self.axes_origin = Point(self.axes_origin[0] + event.rel[0], self.axes_origin[1] + event.rel[1])
        self.update_all_polys(self.axes_origin)
        self.dragStart = Point(event.pos)

    def handle_drag_end(self, event):
        return True

    def assign(self, pos=None):
        if pos is None:
            pos = self.mouse_position

        self.point_list.append(self.translate_to_world(pos, self.axes_origin))

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

    def update_mouse_position(self, event):
        self.mouse_position = event.pos

    def formula(self, point, zmp, newscale=20, oldscale=10):
        def apply_scale(pt, scale):
            return Point(pt[0] * scale, pt[1] * scale)

        if zmp is None:
            zmp = self.axes_origin

        change_in_scale = newscale / oldscale
        value = zmp - ((zmp - point) * change_in_scale)
        compare_val = zmp - apply_scale(zmp - point, change_in_scale)
        assert compare_val == value, f'formula fail, Expected {compare_val}, got {value}'
        # print(f'{point} -> {value}')
        return value

    def update_tick_amount(self, tick_amount=0):
        """ Update scale and axes_origin """
        self.zoom_location = pygame.mouse.get_pos()
        old_scale = round(self.currentTickDistance / self.defaultTickDistance, 2)
        ret = min(self.maxTickSize, max(self.minTickSize, self.currentTickDistance + tick_amount))
        self.currentTickDistance = round(ret, 5)
        new_scale = round(self.currentTickDistance / self.defaultTickDistance, 2)
        new_a_o = self.formula(self.axes_origin, self.zoom_location, new_scale, old_scale)
        self.axes_origin = new_a_o.int()
        self.scale = new_scale
        # ----- TODO: REMOVE -----
        # ----- the rest is adding a triangle to the grid for debugging purposes -----
        if len(self.point_list) < 2:
            self.point_list.clear()
            self.point_list.append(Point(0, 0))
            self.point_list.append(Point(10, 10))
            self.point_list.append(Point(10, 0))
        # ----- TODO: REMOVE -----

    def toggle_fps(self):
        self.showFPS = not self.showFPS

    def next_fps_mode(self):
        self.fpsDisplayMode = (self.fpsDisplayMode + 1) % 15

    def next_error_mode(self):
        self.errorDisplayMode = (self.errorDisplayMode + 1) % 15

    def toggle_static(self):
        self.isInfoStatic = not self.isInfoStatic

    def toggle_grid(self):
        self.showGrid = not self.showGrid

    def toggle_ticks(self):
        self.showTicks = not self.showTicks

    @staticmethod
    def is_left_mouse_button(button):
        return button == BUTTON_LEFT

    @staticmethod
    def is_middle_mouse_button(button):
        return button == BUTTON_MIDDLE

    @staticmethod
    def is_right_mouse_button(button):
        return button == BUTTON_RIGHT

    @staticmethod
    def is_mouse_wheel_up(button):
        return button == BUTTON_WHEELUP

    @staticmethod
    def is_mouse_wheel_down(button):
        return button == BUTTON_WHEELDOWN

    def is_point_on_screen(self, p):
        if p is None or p[0] is None or p[1] is None:
            return False
        return 0 <= p[0] <= self.width and 0 <= p[1] <= self.height

    def get_dot_color(self, p):
        return p[0] % 255, p[1] % 255, 128

    def get_value_from_bits(self, bits, ts1):
        start_x = self.errorPoint[0]
        start_y = self.errorPoint[1]

        box_width = ts1.get_width()
        box_height = ts1.get_height()

        i = bits

        if i & self.BIT_CENTER_HORIZONTALLY:
            start_x = (self.width - box_width) / 2

        if i & self.BIT_CENTER_VERTICALLY:
            start_y = (self.height - box_height) / 2

        box_start_x = start_x
        box_start_y = start_y

        if i & self.BIT_BG_STRETCH_HORIZONTALLY:
            box_start_x = 0
            box_width = self.width

        if i & self.BIT_BG_STRETCH_VERTICALLY:
            box_start_y = 0
            box_height = self.height

        return start_x, start_y, box_start_x, box_start_y, box_width, box_height

    def translate_to_screen(self, p, o=None):
        # if p is None:
        #     raise ValueError(f'Cannot translate None point to screen co-ords')
        #
        # if o is None:
        #     o = self.axes_origin
        #
        # new_x = int((p[0] - o[0]) * self.currentTickDistance + o[0])
        #
        # new_y = int((p[1] - o[1]) * self.currentTickDistance + o[1])
        #
        # # return Point(p[0] * self.currentTickDistance + o[0], -(p[1] * self.currentTickDistance - o[1])).int()
        # return Point(new_x, new_y)
        if o is None:
            o = self.axes_origin

        screen_origin = Point(o)
        world_point = Point(p)
        # print(f't2s-------{world_point=}')
        # Use existing axes_origin to get screen points to correct world point
        origin = Point(0, 0)
        calc_scale = self.currentTickDistance / self.defaultTickDistance * 10
        calc_scale = self.scale * 10
        scale_x = 10
        scale_x = calc_scale
        ' Pixels per unit (integer tick size) f\'{scale_x}\' means 0.0 to 1.0 is 0.1 Pixels, '
        # Should I do this for "flipped" coordinates?
        scale_y = -10
        scale_y = -calc_scale
        rotate = 0.0
        # T-R-S

        r = math.radians(rotate)
        c = math.cos(r)
        s = math.sin(r)

        translated_point = (world_point - origin)
        # transform screen origin relative to
        tra_x = translated_point[0]
        tra_y = translated_point[1]
        # print(f'{translated_point=}')

        rot_x = tra_x * c - tra_y * s
        rot_y = tra_x * s + tra_y * c
        rotated_point = Point(rot_x, rot_y)
        # print(f'{rotated_point=}')

        sca_x = scale_x * rot_x
        sca_y = scale_y * rot_y
        scaled_point = Point(sca_x, sca_y)
        # print(f'{scaled_point=}')

        transformed_point = scaled_point + screen_origin
        # print(f'{transformed_point=}')
        return transformed_point.int()

    def translate_to_world(self, p, o=None):
        # if p is None:
        #     raise ValueError(f'Cannot translate None point to world co-ords')
        #
        # if o is None:
        #     o = self.axes_origin
        #
        # new_x = (p[0] - o[0]) / self.currentTickDistance + o[0]
        # new_y = (p[1] - o[1]) / self.currentTickDistance + o[1]
        #
        # # return Point((p[0] - o[0]) / self.currentTickDistance, -(p[1] - o[1]) / self.currentTickDistance)
        # return Point(new_x, new_y)
        screen_point = Point(p)
        if o is None:
            o = self.axes_origin
        screen_origin = o
        origin = Point(0, 0)
        ' world origin '
        # print(f't2w-------{screen_point=}')

        # Use existing axes_origin to get screen points to correct world point
        origin = Point(0, 0)
        calc_scale = self.scale
        calc_scale = self.currentTickDistance / self.defaultTickDistance * 10
        scale_x = 10
        scale_x = 1 / calc_scale
        ' Pixels per unit (integer tick size) f\'{scale_x}\' means 0.0 to 1.0 is 0.1 Pixels, '
        # Should I do this for "flipped" coordinates?
        scale_y = -10
        scale_y = -1 / calc_scale
        rotate = 0.0
        # T-R-S

        r = math.radians(rotate)
        c = math.cos(r)
        s = math.sin(r)

        translated_point = (screen_point - screen_origin)
        # transform screen origin relative to
        tra_x = translated_point[0]
        tra_y = translated_point[1]
        # print(f'{translated_point=}')

        sca_x = scale_x * tra_x
        sca_y = scale_y * tra_y
        scaled_point = Point(sca_x, sca_y)
        # print(f'{scaled_point=}')

        rot_x = sca_x * c - sca_y * s
        rot_y = sca_x * s + sca_y * c
        rotated_point = Point(rot_x, rot_y)
        # print(f'{rotated_point=}')

        transformed_point = rotated_point + origin
        # print(f'{transformed_point=}')
        return transformed_point

    def mods_value(self, mods):
        return ((0 if mods & KMOD_CTRL or mods & KMOD_SHIFT else 1) +
                (10 if mods & KMOD_CTRL else 0) + (10 if mods & KMOD_SHIFT else 0))

    def input_loop(self):
        keys = pygame.key.get_pressed()  # checking pressed keys
        # print(keys[307], keys[308], len(keys))
        mods = pygame.key.get_mods()  # checking mods held
        pl_new = []
        for pl in self.polygon_list:
            rand_num = random.uniform(-0.4, -0.1)
            pl_new.append(pl.rotate(rand_num))
        self.polygon_list = pl_new

        # if keys[pygame.K_LALT] or keys[pygame.K_RALT]:
        #     self.show_debug_menu = True
        # else:
        #     self.show_debug_menu = False
        if keys[pygame.K_RIGHT]:
            p_list = []
            for p in self.polygon_list:
                # default uses Centroid
                p_list.append(p.rotate(0.25 if mods & KMOD_CTRL else 1))
                # This line rotates around the axes
                # p_list.append(p.rotate(-0.5, self.translate_to_world(self.axes_origin)))
            self.polygon_list = p_list
        elif keys[pygame.K_LEFT]:
            p_list = []
            for p in self.polygon_list:
                p_list.append(p.rotate(-0.25 if mods & KMOD_CTRL else -1))
            # print(p_list)
            # print(self.polygon_list)
            self.polygon_list = p_list
        if mods & KMOD_ALT and mods & KMOD_CTRL and mods & KMOD_SHIFT:
            self.tickAmount = 10
        elif mods & KMOD_CTRL and mods & KMOD_SHIFT:
            self.tickAmount = 2
        elif mods & KMOD_CTRL or mods & KMOD_SHIFT:
            self.tickAmount = 1
        else:
            self.tickAmount = .1

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
                if keys[K_LALT] or keys[K_RALT]:
                    self.show_debug_menu = not self.show_debug_menu
                    # print('Show Debug Menu : ', self.show_debug_menu)
                ap_o = self.translate_to_world(self.axes_origin, self.axes_origin)
                # Press ESCAPE to Quit
                # print(event.key)
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return False
                elif event.key == K_EQUALS:
                    print('K_EQUALS')
                elif event.key == K_KP_MINUS:
                    # print('K_KP_MINUS S')
                    sides = int(event.key - K_0) or 10

                    if self.shape:
                        p = Shape(sides=self.shape.sides,
                                  rot_angle=self.shape.rot_angle,
                                  rot_point=self.shape.rot_point,
                                  radius=self.shape.radius - 1 or 1,
                                  centroid=self.shape.get_centroid())
                        # print(f'self.shape exists{p.radius=} {p}')
                        self.shape = p
                        # print(f'self.shape exists{self.shape=}\nself.shape={self.shape}\n{self.shape.radius=}')
                    # assert self.shape is not None, 'shape not assigned!'

                    # print('K_KP_MINUS E')
                elif event.key == K_MINUS:
                    print('K_MINUS')
                elif event.key == K_KP_PLUS:
                    # print('k_kp_plus S')
                    sides = int(event.key - K_0) or 10

                    if self.shape:
                        p = Shape(sides=self.shape.sides,
                                  rot_angle=self.shape.rot_angle,
                                  rot_point=self.shape.rot_point,
                                  radius=self.shape.radius + 1,
                                  centroid=self.shape.get_centroid())
                        # print(f'self.shape exists{p.radius=} {p}')
                        self.shape = p
                        # print(f'self.shape exists{self.shape=}\nself.shape={self.shape}\n{self.shape.radius=}')
                    # assert self.shape is not None, 'shape not assigned!'
                    # print('k_kp_plus E')
                elif event.key == K_PLUS:
                    # sides = int(event.key - K_0) or 10
                    #
                    # if self.shape:
                    #     p = Shape(sides=self.shape.sides, radius=self.shape.radius + 1,
                    #               centroid=self.translate_to_world(self.mouse_position, self.mouse_position))
                    #     self.shape = p
                    print('K_PLUS')
                elif event.key in [K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9]:
                    p_m = Point(pygame.mouse.get_pos())
                    line = f'screen:{p_m}, world:{self.translate_to_world(p_m, self.axes_origin)}'
                    print(line)
                elif event.key in [K_KP_DIVIDE, K_KP_ENTER, K_KP_EQUALS, K_KP_MINUS, K_KP_PERIOD, K_KP_PLUS,
                                   K_KP_MULTIPLY]:
                    print("KP_SPECIAL", pygame.key.name(event.key))
                elif event.key == K_EQUALS:
                    if mods & KMOD_CTRL:
                        self.largest_polygon += 10
                    if mods & KMOD_ALT:
                        self.largest_polygon += 10
                    if mods & KMOD_SHIFT:
                        self.largest_polygon += 10
                    if not mods:
                        self.largest_polygon += 1
                    self.largest_polygon = self.largest_polygon % 361
                elif event.key == K_MINUS:
                    if mods & KMOD_CTRL:
                        self.largest_polygon -= 10
                    if mods & KMOD_ALT:
                        self.largest_polygon -= 10
                    if mods & KMOD_SHIFT:
                        self.largest_polygon -= 10
                    if not mods:
                        self.largest_polygon -= 1
                    self.largest_polygon = self.largest_polygon % 361
                elif event.key == K_1 and self.largest_polygon >= 3:
                    self.polygon_list.append(Shape(20, self.defaultPolygonRadius, ap_o))
                elif event.key == K_2 and self.largest_polygon >= 3:
                    self.polygon_list.append(Shape(21, self.defaultPolygonRadius, ap_o))
                elif event.key in [K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0]:
                    sides = int(event.key - K_0)
                    s_radius = self.shape.radius if self.shape else 3
                    # print(f'{s_radius=}')
                    if mods & KMOD_CTRL:
                        sides = sides or 10
                        p = Shape(sides=sides, radius=s_radius,
                                  centroid=self.translate_to_world(self.mouse_position, self.mouse_position))
                        self.shape = p
                        self.polygon_list.append(
                            p.translate(self.translate_to_world(self.mouse_position, self.mouse_position)))
                        plg = self.polygon_list[-1]
                        # print('plg', plg)
                    else:
                        sides = sides or 10
                        self.selected_side_count = sides
                        self.shape = Shape(sides=sides, radius=s_radius,
                                           centroid=self.translate_to_world(self.mouse_position, self.mouse_position))

                elif event.key == K_SPACE:
                    if len(self.point_list) >= 3:
                        if mods & KMOD_CTRL:
                            self.polygon_list.append(Shape(self.point_list))
                    elif self.shape:
                        self.polygon_list.append(self.shape.translate(self.mouse_position))
                        self.shape = None
                # Press G to Show Grid
                elif event.key == K_g:
                    self.toggle_grid()
                # Press UP ARROW to increase distance between grid lines
                elif event.key == K_UP:
                    p_list = []
                    for p in self.polygon_list:
                        p_list.append(p.translate((0, 1 if mods & KMOD_CTRL else 10)))
                        # p_list.append(p.translate(self.translate_to_world((0, 1 if mods & KMOD_CTRL else 10))))
                        # p_list.append(p.rotate(0.25, self.translate_to_world(self.axes_origin)))
                    self.polygon_list = p_list
                    # if mods & KMOD_ALT:
                    #     self.map_all_polys(lambda x: x - (self.mods_value(mods), 1))
                    #     self.map_all_polys(lambda y: y - (0, self.mods_value(mods)))
                    # else:
                    #     pass
                # Press DOWN ARROW to decrease distance between grid lines
                elif event.key == K_DOWN:
                    p_list = []
                    for p in self.polygon_list:
                        p_list.append(p.translate((0, -1 if mods & KMOD_CTRL else -10)))
                        # p_list.append(p.rotate(0.25, self.translate_to_world(self.axes_origin)))
                    self.polygon_list = p_list

                    # if mods & KMOD_ALT:
                    #     self.map_all_polys(lambda x: x + (self.mods_value(mods), 0))
                    # else:
                    #     self.map_all_polys(lambda y: y + (0, self.mods_value(mods)))
                elif event.key == K_b:
                    print('NotImplemented! K_b')
                # Press T to show tick marks on axes
                elif event.key == K_t:
                    self.toggle_ticks()
                # Press P to toggle between static and dynamic positioning of data
                elif event.key == K_p:
                    self.toggle_static()
                elif event.key == K_f:
                    self.toggle_fps()
                elif event.key == K_g:
                    self.next_fps_mode()
                elif event.key == K_e:
                    self.next_error_mode()
                elif event.key == K_s:
                    self.showSteps = not self.showSteps
            # ====================
            # MOUSE EVENTS
            # ====================
            # While mouse is moving, keep track of mouse position
            elif event.type == MOUSEMOTION:
                self.update_mouse_position(event)
                self.mouse_move(event)
            # MOUSEBUTTONDOWN events
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_down(event)
            # MOUSEBUTTONUP events
            elif event.type == MOUSEBUTTONUP:
                result = False

                if self.mouse_click_start and (event.button == self.mouse_click_start[1]):
                    self.mouse_click_end = (pygame.time.get_ticks(), event.button)
                    if event.button == self.mouse_click_end[1] == self.mouse_click_start[1]:
                        click_time = self.mouse_click_end[0] - self.mouse_click_start[0]
                        if click_time <= 250:
                            result = self.handle_click(event)

                if not result and self.isDragging:
                    result = self.mouse_drag_end(event)
                    self.dragStart = None
                # If Drag wasn't handled, call mouse_up
                if not result:
                    self.mouse_up(event)
                    self.isHolding = False
                if self.is_mouse_wheel_up(event.button):
                    self.update_tick_amount(self.tickAmount)
                elif self.is_mouse_wheel_down(event.button):
                    self.update_tick_amount(-self.tickAmount)
                elif self.is_middle_mouse_button(event.button):
                    self.toggle_grid()
                else:
                    pass
                self.isHolding = False
                self.isDragging = False
                self.dragStart = None
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
        loop_cnt = 1
        self.print_data['special_menu'] = 'This should be a debug menu\nwith extra\nlines'
        # (self, width, height, vsplit=[], hsplit=[], characterSet=1)
        b = BoxDrawer(10, 9, hsplit=[3, 6])
        self.print_data['special_menu'] = b.as_string(message='File\nEdit\n\nMenu\nOptions\n\nExit')
        while self.input_loop():
            self.Clock.tick()
            curr_time = time.time_ns()
            self.draw_canvas()
            now = time.time_ns()

            loop_cnt = (loop_cnt + 1) % 4

            if not loop_cnt:
                self.print_data['timer'] = (now - curr_time) / 1000000.0

        pygame.quit()
        return


if __name__ == "__main__":
    app = TheWindow()
    # print(app.translate_to_world(app.origin))
    # print(app.translate_to_screen(app.translate_to_world(app.origin)))
    # test_p = Point(-100, 100)
    # print(app.translate_to_world(test_p))
    # print(app.translate_to_screen(app.translate_to_world(test_p)))
    app.run()
