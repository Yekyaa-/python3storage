import math
from typing import Union

import numpy as np
import numpy.linalg as LA


class Point:
    """
    Point class (x, y)
    operators
    Point + Point
    """

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        # if __name__ == "__main__":
        #     print(f"x.setter: Assign {value} to x.")
        if type(value) not in (int, float, None):
            raise ValueError('x.setter: Expecting None, int, or float')
        if type(value) is float:
            self._x = round(value, self.format_digits_to_round)
        else:
            self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        # if __name__ == "__main__":
        #     print(f"y.setter: Assign {value} to y.")
        if type(value) not in (int, float, None):
            raise ValueError('y.setter: Expecting None, int, or float')
        if type(value) is float:
            self._y = round(value, self.format_digits_to_round)
        else:
            self._y = value

    def __init__(self, arg1: Union[int, float, tuple, list] = None, arg2=None):
        """
        if arg1 is tuple, list, or Point, arg2 is ignored.
        """
        self.format_digits_to_round = 7

        if (t_1 := type(arg1)) in (int, float) and type(arg2) in (int, float):
            self.x = arg1
            self.y = arg2
        elif t_1 in (tuple, list, Point) and type(arg1[0]) in (int, float) and type(arg1[1]) in (int, float):
            self.x, self.y = arg1
        elif arg1 is None and arg2 is None:
            self._x = None
            self._y = None
        else:
            raise TypeError('Attempt to init Point with' + str(type(arg1)) + ' and ' + str(type(arg2)))
        # if __name__ == "__main__":
        #     print(f"Created point {self} from {arg1}, {arg2}")

    def __imul__(self, other: Union[tuple, list, float, int]):
        self = self.__mul__(other)
        return self

    def __mul__(self, other: Union[tuple, list, float, int]):
        print('TYPE:OTHER:', type(other), ':', other)
        angle = x = y = extra = None

        if type(other) in (int, float):
            if type(other) is float:
                print('FLOAT WARNING')
            else:
                print('INTEGER WARNING')
            return self.rotate(other)

        try:
            angle, x, y = other
            print(f'NOTICE:***:Unpack succeeded {angle=} {x=} {y=}')
        except ValueError as e:
            try:
                print('NOTICE:***:Unpack failed once')
                angle, extra = other
                print(f'NOTICE:***:Unpack succeeded {angle=} {extra=}')
            except ValueError as e:
                print('NOTICE:***:Unpack failed twice')
                angle = other[0]
                print(f'NOTICE:***:Unpack succeeded {angle=}')
        except TypeError as e:
            print(e.with_traceback(None))
        if extra:
            x, y = extra

        print(f'ROTATING:---:{self=} {angle=} {x=} {y=} {extra=}')

        if type(other) in (float, int):
            return self.rotate(other)
        if type(other) not in (tuple, list):
            raise ValueError('Rotation of a point requires a tuple.')
        if type(other[0]) not in (float, int):
            raise ValueError('Rotation expects angle first.')
        angle = other[0]
        if len(other) == 3 and type(other[1]) in (float, int) and type(other[2]) in (float, int):
            ox = other[1]
            oy = other[2]
        elif len(other) == 2 and hasattr(other[1], '__iter__'):
            ox, oy = other[1]
        else:
            ox = 0
            oy = 0

        return self.rotate(angle, (ox, oy))

    def __sub__(self, other):
        return Point(self.x - other[0], self.y - other[1])

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])

    def __isub__(self, other):
        self.x -= other[0]
        self.y -= other[1]
        return self

    def __iadd__(self, other):
        self.x += other[0]
        self.y += other[1]
        return self

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        if self.x is not None and self.y is not None:
            return True
        return False

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __pos__(self):
        return Point(self.x, self.y)

    @classmethod
    def copy(cls, pt):
        return Point(pt.x, pt.y)

    def __translate__(self, delta_move):
        if not type(delta_move) in (Point, tuple, list):
            raise TypeError('__translate__ accepts Point, tuple, list only')

        delta = Point(delta_move)
        new = self.__add__(delta)

        if __name__ == "__main__":
            print(f'{self} -> {new} :: + Translate {delta}')
        return new

    def __rotate__(self, theta: Union[int, float] = 0, point_of_rotation=(0, 0)):
        rad = math.radians(theta)
        ms = math.sin(rad)
        mc = math.cos(rad)
        x, y = self

        x0, y0 = point_of_rotation
        x -= x0
        y -= y0
        x_prime = x * mc - y * ms
        y_prime = x * ms + y * mc
        x_prime += x0
        y_prime += y0
        x = round(x_prime, self.format_digits_to_round)
        y = round(y_prime, self.format_digits_to_round)

        if x == 0.00000000:
            x = abs(x)
        if y == 0.00000000:
            y = abs(y)

        if __name__ == "__main__":
            print(f'{self} -> {Point(x, y)} :: o Rotate {theta} around ({x0}, {y0})')

        return Point(x, y)

    def __setitem__(self, key, value):
        if key not in [0, 1]:
            return
        if key in [0, 1] and (value is None or value in (float, int)):
            if key:
                self.y = value
            else:
                self.x = value

    def __iter__(self):
        return (val for val in [self.x, self.y])

    def __getitem__(self, item):
        if item is None:
            return None
        if item % 2:
            return self.y
        return self.x

    def __repr__(self):
        return "Point" + self.__str__()

    def __str__(self):
        ret_str = "("
        if self.x is not None:
            ret_str += f" {float(self.x):7.2f}"
        else:
            ret_str += "   None"
        ret_str += ", "

        if self.y is not None:
            ret_str += f" {float(self.y):7.2f}"
        else:
            ret_str += "   None"
        ret_str += ")"
        return ret_str


class Parabola:
    def __translate__(self, item):
        for point in self.known_points:
            print('NOTICE:', type(item), item, len(item))
            point += item
        self.quadratic = self.equation()
        self.generate_list()

    def __rotate__(self, theta, center=(0, 0)):
        for point in self.known_points:
            point.rotate(theta, center)
        self.quadratic = self.equation()
        self.generate_list()

    # Straight lines require 2 points,
    # Anything in a plane requires at least 3.
    def __init__(self, p1=(0, 0), p2=(0, 0), p3=(0, 0), steps=20):
        if p1[0] == p2[0] or p2[0] == p3[0] or p1[0] == p3[0]:
            raise ValueError("Parabola expects all points to have differing x-values!")

        pt_array = [Point(p1), Point(p2), Point(p3)]
        pt_array.sort(key=lambda point: point.x)
        self.known_points = pt_array
        self.angle = math.pi / 2
        self.degrees = math.degrees(self.angle)
        self.slope = 0
        self.change_steps(steps)
        self.quadratic = self.equation()
        self.point_list = self.generate_list()
        self.steps = steps
        self.step_width = (self.known_points[len(self.known_points) - 1].x - self.known_points[0].x) / steps
        self.a = 0
        self.b = 0
        self.c = 0

    def change_steps(self, steps):
        self.steps = steps
        self.step_width = (self.known_points[len(self.known_points) - 1].x - self.known_points[0].x) / steps
        self.quadratic = self.equation()
        self.generate_list()

    def equation(self):
        p1 = self.known_points[0]
        p2 = self.known_points[1]
        p3 = self.known_points[2]

        _A = np.array([[p1.x ** 2, p1.x, 1],
                       [p2.x ** 2, p2.x, 1],
                       [p3.x ** 2, p3.x, 1]])
        _b = np.array([p1.y, p2.y, p3.y]).T
        _x = LA.solve(_A, _b)

        abc = np.array(_x).flatten().tolist()
        self.a, self.b, self.c = abc
        self.slope = 2 * self.a * self.known_points[0].x + self.b
        self.angle = math.atan(self.slope)
        self.degrees = math.degrees(self.angle)
        return "y ={0:8.2f} x\xB2 +{1:8.2f} x +{2:8.2f}".format(self.a, self.b, self.c)

    def step(self, num):
        x = self.known_points[0].x + num * self.step_width
        y = x ** 2 * self.a + x * self.b + self.c
        return Point(x, y)

    def generate_list(self):
        the_list = []
        for i in range(0, self.steps + 1):
            the_list.append(self.step(i))
        # angle = math.fabs(math.degrees(angle))
        # if (not swapped):
        #    slope = -slope
        self.point_list = the_list
        return the_list

    def get_int_list(self):
        the_list = []
        for this_point in self.point_list:
            the_list.append((int(this_point.x), int(this_point.y)))
        return the_list

    def get_list(self):
        the_list = []
        for this_point in self.point_list:
            the_list.append((this_point.x, this_point.y))
        return the_list


def run_point_tests():
    real_point = Point(1, 1)
    center = Point(0.5, 0.5)
    real_point.rotate(30.0)
    real_point.rotate(-30.0)
    real_point.rotate(90)
    real_point.rotate(180)
    real_point.rotate(-90)
    real_point.translate([-100, -100])
    real_point.translate(Point(100, 100))
    g = real_point.rotate(45, center)
    g.rotate(45, center)
    real_point.rotate(45)
    real_point.rotate(-90)
    print(f' Rotation around {center}')
    print('- ' * 20)
    pt_list = [0.5, 0.5]
    pt_tup = (0.5, 0.5)
    real_point * (-90, 0.5, 0.5)
    real_point * (60, center)
    real_point * (30, pt_list)
    print(f'{real_point * (15, pt_tup)=}')
    real_point *= (45, center)
    real_point *= (45, center)
    print()
    print(f' Rotation around ORIGIN')
    print('- ' * 20)
    real_point * [90]
    real_point * -90.0
    fake_point = Point(None, None)
    print(f'{fake_point} is false? {fake_point.__bool__() == False}')
    move_left = real_point + Point(100, 100)

    print(f"{move_left=}")
    print(f"{move_left + (-10, 0)=}")
    xx, yy = move_left
    print(f"{xx=} {yy=} {move_left=}")

    new_pt = Point(xx, yy)
    print(f"{new_pt - move_left=}")


def run_parabola_tests():
    p = Parabola((150, 0), (300, -300), (450, 0), 20)
    for c in p.point_list:
        print(c)
    print(p.step(21))
    print(p.quadratic, end='\n\n')
    p.change_steps(10)
    for c in p.point_list:
        print(c)
    print(p.step(11))
    print(p.quadratic, end='\n\n')
    print(p.known_points)
    print(p.slope, p.angle, p.degrees)
    p.translate([-100, -100])
    print()
    print(p.quadratic)
    print()
    p.rotate(45)
    print()
    print(p.quadratic)
    p.rotate(-45)
    print(p.quadratic)
    try:
        print('Expect error message:p = Parabola((450, 0), (450, 700), (450, 20), 20)')
        Parabola((450, 0), (450, 700), (450, 20), 20)
    except ValueError as e:
        print('Something is wrong!', e)


if __name__ == "__main__":
    # run_parabola_tests()
    run_point_tests()
