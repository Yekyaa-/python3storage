import math
import numpy as np
import numpy.linalg as LA

from python3storage.Classes.Point import Point


class Parabola:
    def translate(self, lst):
        for c in self.known_points:
            c.translate(lst)
        self.quadratic = self.equation()
        self.generate_list()

    def rotate(self, theta):
        for c in self.known_points:
            c.rotate(theta)
        self.quadratic = self.equation()
        self.generate_list()

    # Straight lines require 2 points,
    # Anything in a plane requires at least 3.
    def __init__(self, p1, p2, p3, steps):
        Point.fromtuple((1, 0))
        if p1[0] == p2[0] or p2[0] == p3[0] or p1[0] == p3[0]:
            raise ValueError("Parabola expects all points to have differing x-values!")
        pt_array = [Point.fromtuple(p1), Point.fromtuple(p2), Point.fromtuple(p3)]
        pt_array.sort(key=lambda point: point.x)
        self.known_points = pt_array
        self.angle = math.pi / 2
        self.degrees = math.degrees(self.angle)
        self.slope = 0
        self.change_steps(steps)
        self.quadratic = self.equation()

    def change_steps(self, steps):
        self.steps = steps
        self.stepwidth = (self.known_points[len(self.known_points) - 1].x - self.known_points[0].x) / steps
        self.quadratic = self.equation()
        self.generate_list()

    def equation(self):
        p1 = self.known_points[0]
        p2 = self.known_points[1]
        p3 = self.known_points[2]

        _A = np.matrix([[p1.x ** 2, p1.x, 1],
                        [p2.x ** 2, p2.x, 1],
                        [p3.x ** 2, p3.x, 1]])
        _b = np.matrix([p1.y, p2.y, p3.y]).transpose()
        _x = LA.solve(_A, _b)

        self.a, self.b, self.c = np.array(_x).flatten().tolist()
        self.slope = 2 * self.a * self.known_points[0].x + self.b
        self.angle = math.atan(self.slope)
        self.degrees = math.degrees(self.angle)
        return "y ={0:8.2f} x\xB2 +{1:8.2f} x +{2:8.2f}".format(self.a, self.b, self.c)

    def step(self, num):
        x = self.known_points[0].x + num * self.stepwidth
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
        return

    def get_list(self):
        the_list = []
        for p in self.point_list:
            the_list.append((p.x, p.y))
        return the_list


if __name__ == "__main__":
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
        p = Parabola((450, 0), (450, 700), (450, 20), 20)
    except ValueError as e:
        print('Something wrong!', e)
    Pxy = Point(2, 1)
    # print(Pxy)
    Pxy.translate([100, 100])
    Pxy.rotate(30.0)
    Pxy.rotate(-30.0)
    Pxy.rotate(90)
    Pxy.rotate(-90)
    Pxy.translate([-100, -100])
    Pxy.rotate(45)
    Pxy.rotate(45)
    Pxy.rotate(180)
    Pxy.rotate(-90)
    