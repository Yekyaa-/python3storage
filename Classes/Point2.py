import math
from typing import Union


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

    def get_angle_axes(self, other):
        if __name__ == "__main__":
            print(f' MUL:{type(other)=}:>{other=}<')

        angle = x = y = extra = None

        if type(other) in (int, float):
            if __name__ == "__main__":
                print(f' MUL:warning:{type(other)=} ROTATING:{self=} * angle={other}')
            return self.__rotate__(other)

        try:
            angle, x, y = other
            if __name__ == "__main__":
                print(f'NOTICE:***:Unpack succeeded {angle=} {x=} {y=}')
        except ValueError as _:
            try:
                angle, extra = other
                if __name__ == "__main__":
                    print(f'NOTICE:***:Unpack succeeded {angle=} {extra=}')
            except ValueError as _:
                angle = other[0]
                if __name__ == "__main__":
                    print(f'NOTICE:***:Unpack succeeded {angle=}')
        except TypeError as e:
            print(e.with_traceback(None))
        if extra:
            x, y = extra

        if __name__ == "__main__":
            print(f'ROTATING:---:{self=} {angle=} {x=} {y=} {extra=}')

        if type(other) in (float, int):
            return self.__rotate__(other)
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
        return tuple(angle, (ox, oy))

    def __matmul__(self, other):
        """
        Matrix Multiply @
        """
        return other

    def __imatmul__(self, other):
        """
        Inline Matrix Multiply @=
        """
        return other

    def __imul__(self, other: Union[tuple, list, float, int]):
        # noinspection PyMethodFirstArgAssignment
        if __name__ == "__main__":
            print('IMUL:TYPE:', type(other), ':OTHER:', other)

        return self.__mul__(other)

    def __mul__(self, other: Union[tuple, list, float, int]):
        return self.__rotate__(*self.get_angle_axes(other))

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
        return Point(pt)

    def __translate__(self, delta_move):
        if not type(delta_move) in (Point, tuple, list):
            raise TypeError('__translate__ accepts Point, tuple, list only')

        delta = Point(delta_move)
        new = self.__add__(delta)

        if __name__ == "__main__":
            print(f'{self} -> {new} :: + Translate {delta}')
        return new

    def __rotate__(self, theta: Union[int, float] = 0, point_of_rotation=None):
        if point_of_rotation is None:
            raise ValueError('point_of_rotation is required!')
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

    def round(self, digits=3):
        if digits:
            return Point(round(self.x, digits), round(self.y, digits))
        return Point(int(self.x), int(self.y))

    def __getitem__(self, item):
        if item is None:
            return None
        if item % 2:
            return self.y
        return self.x

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

    def __len__(self):
        return [self.x, self.y].__len__()

    def __repr__(self):
        return "Point" + self.__str__()

    def __str__(self):
        ret_str = "("
        if self.x is not None:
            ret_str += f" {float(self.x):7.7f}"
        else:
            ret_str += "   None"
        ret_str += ", "

        if self.y is not None:
            ret_str += f" {float(self.y):7.7f}"
        else:
            ret_str += "   None"
        ret_str += ")"
        return ret_str

    def is_valid(self):
        if self is None or (self[0] is None and self[1] is None):
            return False
        return True

    def __init__(self, arg1: Union[int, float, tuple, list] = None, arg2=None):
        """
        if arg1 is tuple, list, or Point, arg2 is ignored.
        """
        self.format_digits_to_round = 7
        if __name__=="__main__":
            print(f'Point():{type(arg1)=}:{arg1=}', end='')

        if (t_1 := type(arg1)) in (int, float) and type(arg2) in (int, float):
            if __name__ == "__main__":
                print(f':{type(arg2)=}:{arg2=}')
            self.x = arg1
            self.y = arg2
        elif t_1 in (tuple, list, Point) and type(arg1[0]) in (int, float) and type(arg1[1]) in (int, float):
            self.x, self.y = arg1
            if __name__ == "__main__":
                if t_1 is tuple:
                    print(f'|TUPLE({type(self.x)}, {type(self.y)})')
                elif t_1 is Point:
                    print(f'|POINT<{type(self.x)}, {type(self.y)}>')
                elif t_1 is list:
                    print(f'|LIST[{type(self.x)}, {type(self.y)}]')
        elif arg1 is None and arg2 is None:
            self._x = None
            self._y = None
            if __name__ == "__main__":
                print(f':NONE/NONE,NONE/(NONE,NONE)/[NONE,NONE]:<<{type(self.x)}, {type(self.y)}>>')
        else:
            raise TypeError('Attempt to init Point with' + str(type(arg1)) + ' and ' + str(type(arg2)))
        # if __name__ == "__main__":
        #     print(f"Created point {self} from {arg1}, {arg2}")



def run_point_tests():
    real_point = Point(1, 1)
    center = Point(0.5, 0.5)
    real_point.__rotate__(30.0)
    real_point.__rotate__(-30.0)
    real_point.__rotate__(90)
    real_point.__rotate__(180)
    real_point.__rotate__(-90)
    real_point.__translate__([-100, -100])
    real_point.__translate__(Point(100, 100))
    g = real_point.__rotate__(45, center)
    g.__rotate__(45, center)
    real_point.__rotate__(45)
    real_point.__rotate__(-90)
    print(f' Rotation around {center}')
    print('- ' * 20)
    pt_list = [0.75, 0.75]
    pt_tup = (0.5, 0.5)
    print('-' * 15 + 'Three Rotations' + '-' * 15)
    real_point * (-90, 0.5, 0.5)
    real_point * (60, center)
    real_point * (30, pt_list)
    print('-' * 15 + 'Tuple' + '-' * 15)
    print(f'{real_point * (15, pt_tup)=}')
    print('-' * 15 + 'Point Thrice' + '-' * 15)
    real_point *= (45, center)
    real_point *= (45, center)
    real_point *= (-90, center)
    print()
    print(f' Rotation around ORIGIN')
    print('- ' * 20)
    print('-' * 15 + 'List of 1 Int' + '-' * 15)
    real_point * [90]
    print('-' * 15 + 'Float' + '-' * 15)
    real_point * -90.0
    print('-' * 15 + ' Int ' + '-' * 15)
    real_point * 180
    print('-' * 15 + ' Fake Point Test ' + '-' * 15)
    fake_point = Point(None, None)
    print(f'{fake_point} is false? {fake_point.__bool__() == False}')
    print()
    real_point *= (90, center)
    print(f'Translation {real_point}')
    print('-' * 15 + 'Point' + '-' * 15)
    move_left = real_point + Point(100, 100)
    print('move_left=real_point + Point(100, 100)')
    print(f"{move_left=}")

    print('-' * 15 + 'Tuple' + '-' * 15)
    print(f"{move_left + (-10, 0)=}")

    print('-' * 15 + 'List' + '-' * 15)
    move_left = real_point + [100, 100]

    print(f'Iteration')
    print('-' * 15 + 'Unpacking' + '-' * 15)
    xx, yy = move_left
    print(f"{xx=} {yy=} {move_left=}")

    new_pt = Point(xx, yy)
    print(f"{new_pt - move_left=}")

    print('-- Point(LIST[]) --')
    new_pt_3 = Point([-3.555, 10])
    print()
    print('-- Point(Tuple()) --')
    new_pt_3 = Point((-4, -1.333))
    print()
    print('-- Point(Point<>) --')
    new_pt_3 = Point(new_pt)
    print()


if __name__ == "__main__":
    run_point_tests()
