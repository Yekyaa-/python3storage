import math
from typing import Union


class CJLogIt:
    def __init__(self, funcname='', textparams='', e='', en='\n'):
        self.f = funcname
        self.t = textparams
        self.e = e
        self.en = en

    def update(self, f=None, t=None, e=None, en='\n'):
        self.f = f or self.f
        self.t = t or self.t
        self.e = e or self.e
        self.en = en or self.en

    def print(self, rest_of_msg='', f=None, t=None, e=None, end='\n'):
        if __name__ == "__main__":
            f = f or self.f
            t = t or self.t
            e = e or self.e
            en = end or self.en
            print(f'Point.{f}:{t}:{e}:{rest_of_msg}{en}', end='')


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
        if type(value) not in (int, float) and value is not None:
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
        if type(value) not in (int, float) and value is not None:
            raise ValueError('y.setter: Expecting None, int, or float')
        if type(value) is float:
            self._y = round(value, self.format_digits_to_round)
        else:
            self._y = value

    def calc_radius(self, other):
        self.log.update(f='calc_radius')
        x1 = self[0]
        y1 = self[1]
        if other:
            x2 = other[0]
            y2 = other[1]
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        else:
            raise ValueError(f'None not allowed when determining radius!')

    def int(self):
        return Point(int(self._x), int(self._y))

    def round(self, digits=None):
        # is it just a super small value?
        # Return int
        # otherwise, round to expected digits
        _x = self._x
        _y = self._y

        do_round_x = True if _x else False
        do_round_y = True if _y else False

        digits = digits if digits is not None and digits >= 0 else 10

        if digits:
            delta = 5 / (10 ** (digits + 1))
        else:
            delta = 0

        if do_round_x:
            x_s = f'{_x}'
            if type(_x) is int:
                _x = float(_x)
            if not digits or -delta < _x < delta or (-5e-9 < _x < 5e-9 and int(x_s[-2:]) >= self.format_digits_to_round):
                _x = int(_x)
            else:
                _x = round(_x, digits)

        if do_round_y:
            if type(_y) is int:
                _y = float(_y)

            y_s = f'{_y}'

            if not digits or -delta < _y < delta or (-5e-9 < _y < 5e-9 and int(y_s[-2:]) >= self.format_digits_to_round):
                _y = int(_y)
            else:
                _y = round(_y, digits)

        return Point(_x, _y)

    def _old_round(self, digits=None):
        if digits is None:
            digits = self.format_digits_to_round

        x, y = None, None

        if digits:
            if digits > 1:
                delta = 5 / (10 ** self.format_digits_to_round)
            else:
                delta = digits

            # print('delta, format_digits', format(delta, '7.11f'), self.format_digits_to_round)

            if self._x is not None:
                x = round(self._x, digits)
            else:
                x = self._x

            if self._y is not None:
                y = round(self._y, digits)
            else:
                y = self._y

            if -delta <= (x - int(x)) <= delta:
                tmp_x = round(x, digits - 1)
                tmp_y = round(y, digits - 1)
                x_s = f'{x}'
                y_s = f'{y}'
                tmp_x_s = f'{tmp_x}'
                tmp_y_s = f'{tmp_y}'
                e_in_x = 'e' in x_s
                e_in_y = 'e' in y_s
                e_in_tmp_x = 'e' in tmp_x_s
                e_in_tmp_y = 'e' in tmp_y_s
                if e_in_x or e_in_y or e_in_tmp_x or e_in_tmp_y:
                    assert e_in_x, f'{x=} integer? {x.is_integer()}'
                    assert e_in_y, f'{y=} integer? {y.is_integer()}'
                    # is_it_bad = f'Round from {digits} to {digits - 1} '
                    # is_it_bad += f'({x} {e_in_x} -> {tmp_x=} {e_in_tmp_x=},'
                    # is_it_bad += f'{y} -> {tmp_y} {e_in_y=} {e_in_tmp_y=})'
                    # print(is_it_bad)
                    tmp_tmp_y = tmp_y
                    tmp_tmp_x = tmp_x
                    if e_in_tmp_x:
                        tmp_tmp_x = round(x, digits - 2)
                        tmp_tmp_x_s = f'{tmp_tmp_x}'
                        print(f'__round__** ADJUSTED X-VALUE from {x} -> {tmp_x} -> {tmp_tmp_x}')
                        assert 'e' not in tmp_tmp_x_s, f'e found in tmp_tmp_x'
                        assert not e_in_tmp_x, 'FIXED THE ISSUE, HERE IS WHERE IT IS FROM'
                    else:
                        assert not e_in_tmp_x, 'e found in tmp_x'
                    if e_in_tmp_y:
                        tmp_tmp_y = round(y, digits - 2)
                        tmp_tmp_y_s = f'{tmp_tmp_y}'
                        print(f'__round__** ADJUSTED Y-VALUE from {y} -> {tmp_y} -> {tmp_tmp_y}')
                        assert 'e' not in tmp_tmp_y_s, f'e found in tmp_tmp_y'
                    else:
                        assert not e_in_tmp_y, 'e found in tmp_y'
                x = tmp_x
                y = tmp_y

        return Point(x, y)
        #    return Point(int(self.x), int(self.y))

    # noinspection PyMethodMayBeStatic
    def get_theta_xy(self, other):
        # self op_code other
        self.log.update(f='get_theta_xy')
        header = f'{self}:{other}-->*'
        # self op_code 2.0
        if type(other) in [float, int]:
            self.log.print(f'{header}:{other}, 0, 0')
            return other, 0, 0
        # self op_code (2.0)
        elif type(other) in [tuple]:
            theta, xy = other
            if type(xy) in [tuple, list, Point]:
                x, y = xy
                self.log.print(f'{header}:{theta}, {x}, {y}')
                return theta, x, y
            elif xy is None:
                x = 0
                y = 0
                self.log.print(f'{header}:{theta}, {x}, {y}')
                return theta, x, y
            else:
                raise ValueError(f'Unexpected format ({theta}, {xy.__repr__()})')
        else:
            raise ValueError(f'Unexpected format: {other.__repr__()}')

    def __imatmul__(self, other):
        theta, ox, oy = self.get_theta_xy(other)
        self.log.update(f='__imatmul__')
        if math.fmod(round(theta, 7), 360.0000000) == 0.0000000:
            return self

        rad = math.radians(theta)
        ms = math.sin(rad)
        mc = math.cos(rad)

        x = self._x
        y = self._y

        dx = x - ox
        dy = y - oy

        x_prime = dx * mc - dy * ms
        y_prime = dx * ms + dy * mc

        x_f = x_prime + ox
        y_f = y_prime + oy

        x = round(x_f, self.format_digits_to_round)
        y = round(y_f, self.format_digits_to_round)

        if round(x, 7) == 0.0000000:
            x = abs(x)
        if round(y, 7) == 0.0000000:
            y = abs(y)

        line = f'{self} -> ({x}, {y}) :: o Rotate {theta} around ({ox}, {oy})'
        line += f' ==>> [T({dx}, {dy})->R({x_prime}, {y_prime})->T({x_f}, {y_f})]'
        self.log.print(line)

        self.x = x
        self.y = y
        return self

    def __matmul__(self, other=None):
        theta, ox, oy = self.get_theta_xy(other)
        self.log.update(f='__matmul__')
        if math.fmod(round(theta, 7), 360.0000000) == 0.0000000:
            return Point(self.x, self.y)

        rad = math.radians(theta)
        ms = math.sin(rad)
        mc = math.cos(rad)

        x = self._x
        y = self._y

        dx = x - ox
        dy = y - oy

        x_prime = dx * mc - dy * ms
        y_prime = dx * ms + dy * mc

        x_f = x_prime + ox
        y_f = y_prime + oy

        x = round(x_f, self.format_digits_to_round)
        y = round(y_f, self.format_digits_to_round)

        if round(x, 7) == 0.0000000:
            x = abs(x)
        if round(y, 7) == 0.0000000:
            y = abs(y)

        ret = Point(x, y)

        line = f'{self} -> {ret} :: o Rotate {theta} around ({ox}, {oy})'
        line += f' ==>> [T({dx}, {dy})->R({x_prime}, {y_prime})->T({x_f}, {y_f})]'
        self.log.print(line)

        return ret

    def rotate(self, theta, o_pt=None):
        assert theta is not None, 'theta is None! ^^^'
        return self @ (theta, o_pt)

    def __radd__(self, other):
        self.log.update('__radd__')
        """
        Reverse Addition. (x, y) or [x, y] + Point()
        Returns new Point representing the combination.
        Args:
            other: tuple(2) or list(2) of int/float
        Returns:
            Point
        """
        self.log.print(f'{self} {other}')

        if other is not None:
            self.log.print(f'{type(other)=}{other=}')
            return Point(self.x + other[0], self.y + other[1])
        return Point(self)

    def __add__(self, other):
        """
        Addition. Point() + OtherPoint()
        Returns new Point representing the combination.
        Args:
            other: Point or tuple(2) or list(2) of int/float
        Returns:
            Point
        """
        self.log.update('__add__')
        self.log.print(f'{self} {other}')

        if other is not None:
            return Point(self.x + other[0], self.y + other[1])
        return Point(self)

    def __iadd__(self, other):
        """
        Inline Addition. Point() += OtherPoint()
        Modifies Point()
        Args:
            other: Point or tuple(2) or list(2) of int/float
        Returns:
            Point
        """
        self.log.update('__iadd__')
        self.log.print(f'{self} {other}')
        if other is not None:
            self.x = self.x + other[0]
            self.y = self.y + other[1]
        return self

    def __rsub__(self, other):
        """
        Reverse Subtraction. (x, y) or [x, y] - Point()
        Returns new Point representing the difference.
        Args:
            other: Point or tuple(2) or list(2) of int/float
        Returns:
            Point
        """
        self.log.update('__rsub__')
        self.log.print(f'{self} {other}')
        if other is not None:
            return Point(other[0] - self.x, other[1] - self.y)
        return Point(self.__neg__())

    def __sub__(self, other):
        self.log.update('__sub__')
        """
        Subtraction. Point() - OtherPoint()
        Returns new Point representing the difference.
        Args:
            other: Point or tuple(2) or list(2) of int/float
        Returns:
            Point
        """
        self.log.print(f'{self} {other}')
        if other is not None:
            return Point(self.x - other[0], self.y - other[1])
        return Point(self)

    def __isub__(self, other):
        """
        Inline Subtraction. Point() -= OtherPoint()
        Modifies Point()
        Args:
            other: Point or tuple(2) or list(2) of int/float
        Returns:
            Point
        """
        self.log.update('__isub__')
        self.log.print(f'{self} {other}')
        if other is not None:
            self.x = self.x - other[0]
            self.y = self.y - other[1]
        return self

    def translate(self, o_pt):
        self.log.update('translate')
        self.log.print(f'Point({self.x}, {self.y}) + ({o_pt[0]}, {o_pt[1]})')
        return self + o_pt

    def __rtruediv__(self, other):
        raise NotImplementedError('Division of a point is not defined. Did you mean to scale (*) ?')

    def __truediv__(self, other):
        raise NotImplementedError('Division on a point is not defined. Did you mean to scale (*) ?')

    def __idiv__(self, other):
        raise NotImplementedError('Division on a point is not defined. Did you mean to scale (*) ?')

    def __mul__(self, other):
        """ Scale : Point * { 'factor': required, 'origin' : required } """

        x = self.x
        y = self.y
        ox = oy = 0.0

        if type(other) in [int, float]:
            factor_x = factor_y = other
        elif type(other) in [Point, tuple, list]:
            part1, part2 = other
            ox, oy = part2
            if type(part1) in [int, float]:
                factor_x = factor_y = part1
            elif type(part1) in [Point, tuple, list]:
                factor_x, factor_y = part1

        dx = x - ox
        dy = y - oy

        x_prime = dx * factor_x
        y_prime = dy * factor_y

        x_f = x_prime + ox
        y_f = y_prime + oy

        x = round(x_f, self.format_digits_to_round)
        y = round(y_f, self.format_digits_to_round)

        if round(x, 7) == 0.0000000:
            x = abs(x)
        if round(y, 7) == 0.0000000:
            y = abs(y)

        return Point(x, y)

    def super__mul__(self, other):
        """
        Point * (Factor, Point)                                             \
        Point * Factor                                                      \
        Point * {'factor': factor_int: 'origin': origin_Point}              \
        Point * {'factor': (factor_x, factor_y), 'origin': origin_Point}
        Args:
            other:
        Returns:
        """
        self.log.update('__mul__')

        # Must be of these types to be supported
        assert type(other) in [int, float, Point, list, tuple, dict], f'Cannot scale with given type of {type(other)}'

        # Break down other to retrieve factor and/or origin
        if type(other) in [int, float]:
            # Factor is the only thing allowed as an integer
            other = {'factor': other}
        elif type(other) in [Point, list, tuple]:
            a, b = other
            assert type(a) in [int, float, tuple, Point, list], str(type(a))
            assert type(b) in [tuple, Point, list], str(type(b))
            other = {'factor': a, 'origin': b}

        assert type(other) is dict, 'Dictionary with keys \'factor\' and/or \'origin\' expected!'
        self.log.print('other:', other)
        assert 'factor' in other.keys(), 'Scaling factor required!'

        if 'factor' not in other.keys():
            other['factor'] = 1.0

        if 'origin' not in other.keys():
            other['origin'] = (0, 0)

        val = other['factor']
        org = other['origin']

        assert type(other['factor']) in [Point, list, tuple, int, float], f'Factor must be sequence, int, or float'
        assert type(other['origin']) in [tuple, list, Point], f'Origin must be a Point, list, or tuple'

        if type(val) in [Point, list, tuple]:
            factor_x = val[0]
            factor_y = val[1]
        elif type(val) in [int, float]:
            factor_x = val
            factor_y = val

        if type(org) in [Point, list, tuple]:
            ox = org[0]
            oy = org[1]

        x = self.x
        y = self.y

        dx = x - ox
        dy = y - oy

        x_prime = dx * factor_x
        y_prime = dy * factor_y

        x_f = x_prime + ox
        y_f = y_prime + oy

        x = round(x_f, self.format_digits_to_round)
        y = round(y_f, self.format_digits_to_round)

        if round(x, 7) == 0.0000000:
            x = abs(x)
        if round(y, 7) == 0.0000000:
            y = abs(y)

        ret = Point(x, y)

        line = f'{self} -> {ret} :: o Scale {factor_x, factor_y} around {ox, oy}'
        line += f' ==>> [T{dx, dy}->S{x_prime, y_prime}->T{x_f, y_f}]'
        self.log.print(line)

        return ret

    def __imul__(self, other):
        return self * other

    def scale(self, factor, o_pt):
        return self * (factor, o_pt) if o_pt else factor

    def __round__(self, digits=0):
        self.log.update('__round__')
        header = f'{self}:{digits}:'
        if digits:
            self.log.print(f'{header}({round(self.x, digits)}, {round(self.y, digits)})')
            return Point(round(self.x, digits), round(self.y, digits))
        self.log.print(f'{header}({int(self.x)}, {int(self.y)})')
        return Point(int(self.x), int(self.y))

    def __eq__(self, other):
        self.log.update('__eq__')
        try:
            val = (self.x == other[0]) and (self.y == other[1])
            self.log.print(f'{self} == {other}? {val}')
        except TypeError:
            raise AssertionError('STOP AND FIX THIS! ^^^')
        return val

    def __ne__(self, other):
        val = self.__eq__(other)
        self.log.update('__ne__')
        self.log.print(f'{self}:{other}:{not val}')
        return not val

    def __bool__(self):
        self.log.update('__bool__')
        self.log.print(f'{self}', end='')
        if self.x is not None and self.y is not None:
            self.log.print(':True')
            return True
        self.log.print(':False')
        return False

    def __neg__(self):
        self.log.update('__neg__')
        self.log.print(f'{self} -> {(-self.x, -self.y)}')
        return Point(-self.x, -self.y)

    def __pos__(self):
        self.log.update('__pos__')
        self.log.print(f'{self}')
        return self

    def __len__(self):
        """
        COMPLETED
        Get the number of items in the Point
        Returns:
            2.  It's so random, it's not!
        Throws:
            Nothing, this function LITERALLY returns the number 2.
        """
        self.log.update('__len__')
        self.log.print(f'{self} only has {self._len} parts.')
        return self._len

    def __getitem__(self, key: int):
        """
        COMPLETED
        Get the value found at location pointed to by 'key'.
        Returns:
            float value located at location 'key'
        Throws:
            Throws IndexError if 'key' does not exist.
        """
        self.log.update('__getitem__')
        header = f'{self}[{key}]:'

        if key in [0, -2]:
            self.log.print(header + ' is ' + str(self.x))
            return self.x
        elif key in [-1, 1]:
            self.log.print(header + 'is ' + str(self.y))
            return self.y
        elif key == 2:
            self.log.print(header + ' End of Loop Sequence Flag -- IndexError')
            raise IndexError(f'{key} does not exist!')
        else:
            self.log.print(header + ' Unknown Reason but here   -- IndexError')
            raise IndexError(f'{key} does not exist!')

    def __hash__(self):
        """
        For dictionary storing, and probably other things, but this was the first error.
        Returns:
            hash(tuple(self._x, self._y)) + 1
        """
        return hash((self._x, self._y))

    def __setitem__(self, key: int, value: Union[int, float]):
        """
        COMPLETED
        Set the value found at location pointed to by 'key' to 'value'.
        Returns:
            nothing
        Throws:
            Throws IndexError if 'key' does not exist.
            Throws TypeError if value is not int/float
        """
        self.log.update('__setitem__')
        header = f'{self}[{key}] = {value} from '

        if (value is None) or (type(value) in (float, int)):
            if key in [0, -2]:
                self.log.print(header + str(self.x))
                self._x = round(value, self.format_digits_to_round)
            elif key in [-1, 1]:
                self.log.print(header + str(self.y))
                self._y = round(value, self.format_digits_to_round)
            else:
                self.log.print(header + ' End of Loop Sequence Flag -- IndexError')
                raise IndexError(f'{key} does not exist!')
        else:
            self.log.print(' TypeError')
            raise TypeError(f'{value} is not int or float!')

    def __delitem__(self, key: int):
        """
        COMPLETED
        Set the value found at location pointed to by 'key' to None.
        Returns:
            nothing
        Throws:
            Throws IndexError if 'key' does not exist.
        """
        self.log.update('__delitem__')
        self.log.print(f'{self}[{key}] from {self.x if key in [0, -2] else self.y} to None')

        if key in [0, -2]:
            self._x = None
        elif key in [-1, 1]:
            self._y = None
        else:
            raise IndexError(f'{key} does not exist!')

    def __abs__(self):
        """
        COMPLETED
        Returns:
            Returns a Point(x, y) object where x and y are >= 0
        """
        self.log.update('__abs__')
        self.log.print(f'{self}')
        return Point(abs(self.x), abs(self.y))

    def __repr__(self):
        """
        COMPLETED
        Returns:
            Returns a string representation of the Point(x, y) object for reproducing.
        """
        return "Point" + self.__str__()

    def __format__(self, format_spec=''):
        """
        COMPLETED
        Returns:
            Returns a string representation of the Point(x, y) object using float format specifiers
        """
        return f'({format(self._x, format_spec)}, {format(self._y, format_spec)})'

    def __str__(self):
        """
        COMPLETED
        Returns:
            Returns a string representation of the Point(x, y) object
        """
        return self.__format__()

    def __init__(self, arg1: Union[int, float, tuple, list] = None, arg2: Union[int, float] = None):
        self.log = CJLogIt('__init__')
        """
        if arg1 is tuple, list, or Point, arg2 is ignored.
        if arg1 is int/float, arg2 must a int/float
        """
        t1 = type(arg1)
        t2 = type(arg2)

        self._len = 2
        """The literal "length" of a single point is how many dimensions are required to represent it."""
        self.format_digits_to_round = 10

        if (arg1 is None or t1 in (int, float)) and (arg2 is None or t2 in (int, float)):
            self.x = arg1
            self.y = arg2
        elif t1 in (tuple, list, Point) and arg2 is None:
            self.x = arg1[0]
            self.y = arg1[1]
        else:
            raise TypeError(f'{t1=} {t2=} {t1 in (tuple, list, Point)=} {arg2 is None=}')
        self.log.print(f'Point created successfully! {self}, {arg1=}, {arg2=}')


def run_point_tests():
    tup = (11, 5)
    lst = [12, 7]

    print('\n-- BASIC CREATION --')
    center = Point(0, 0)

    print('\n--  TUPLE CONVERSION --')
    pt_tup = Point(tup)

    print('\n--  LIST CONVERSION --')
    pt_lst = Point(lst)

    print('\n-- POINT CONVERSION & CREATION--')
    blank_pt = Point(None, None)
    print('-- pt_pt = Point(pt_lst)')
    pt_pt = Point(pt_lst)
    print('-- SEQUENCE # 1 --')
    pt_pt[1] = 8
    print(pt_pt)
    print('-- SEQUENCE # 2 --')
    pt_pt[1] = 7
    print(pt_pt)

    print('\n-- [in]EQUALITY TESTS --')
    print('pt_lst v tup')
    assert pt_lst != tup
    print('pt_lst v lst')
    assert pt_lst.__ne__(lst) is False
    print('pt_tup v lst')
    assert pt_tup != lst
    print('pt_tup v tup')
    assert pt_tup.__ne__(tup) is False
    print('pt_pt v pt_lst')
    assert pt_pt == pt_lst

    print('\n-- BOOL CHECK --')
    assert not blank_pt.__bool__()
    assert pt_tup.__bool__()
    assert center.__bool__()

    print('\n-- NORMY INIT TEST --')
    pt_int = Point(100, -100)
    pt_flt = Point(0.5, 0.5)
    pt_f_i = Point(0.333, 250)
    pt_i_f = Point(251, 0.3349)
    print('\n-- NEG TEST --')
    assert -pt_f_i == (-0.333, -250)

    print('\n-- LEN TEST --')
    assert len(pt_f_i) == 2, 'SHOULD BE 2'

    print('\n-- ROUND --')
    assert round(pt_i_f, 3) == (251, 0.335000), 'SHOULD NOT BE BROKEN!'
    assert round(pt_i_f) == (251, 0), 'SHOULD NOT BE BROKEN!'

    print('\n-- ABS --')
    assert abs(pt_int) == (100, 100), 'SHOULD BE EQUAL'

    print('\n-- ADD OPERATIONS --')
    u = pt_lst + tup
    v = tup + pt_lst
    assert u == v, f'{u} == {v}, Expected True, got {u == v}'

    r = pt_tup + lst
    s = lst + pt_tup
    assert r == s, f'{r} == {s}, Expected True, got {r == s}'

    print('\n-- SUB OPERATIONS --')
    # 12, 7 - 11, 5 = 1, 2
    r = pt_lst - tup
    assert r == (1, 2), f'{pt_lst} - {tup} Expected (1, 2), got {r}'

    # 11, 5 - 12, 7 = -1, -2
    r = tup - pt_lst
    assert r == (-1, -2), f'{tup} - {pt_lst} Expected (-1, -2), got {r}'

    r = pt_tup - lst
    assert r == (-1, -2), f'{pt_tup} - {lst} Expected (-1, -2), got {r}'

    r = lst - pt_tup
    assert r == (1, 2), f'{lst} - {pt_tup} Expected (1, 2), got {r}'

    # Must create new object, not link to old one
    r = Point(pt_lst)
    r -= lst
    assert r == (0, 0), 'SHOULD BE (0, 0)'

    print('\n-- STR FUNCS --')
    print(f'{pt_i_f.__str__()=}')
    print(f'{pt_i_f.__repr__()=}')
    print(f'{pt_i_f=}')

    print('\n-- DATA --')
    print(f'{tup=} {lst=} {pt_tup=} {pt_lst=}')

    print('\n-- GETITEM --')
    assert tup[0] == pt_tup[0], 'SHOULD BE SAME X'
    assert lst[1] == pt_lst[1], 'SHOULD BE SAME Y'
    assert Point(12, None) == (12, None), 'SHOULD BE (12, None)'

    print('\n-- DELITEM SETITEM--')
    print('del')
    del pt_lst[1]
    print('set')
    pt_lst[1] = -11
    print('assert')
    assert pt_lst == (12, -11), 'SHOULD BE (12, -11)'

    print('\n-- ITER TEST --')
    for c in pt_lst:
        print('Print Statement: Value is ', c)
    else:
        print('&&& *** Seen At A Park: The Else on a For Statement is just an except IndexError -- Change My Mind.')

    print('\n-- ROTATION TEST --')
    zero = (0, 0)
    half = (0.5, 0.5)
    assert Point(1, 1).rotate(90, zero) == (-1, 1)
    assert Point(1, 1).rotate(90, half) == (0, 1)
    assert Point(1, 1).rotate(180, half) == (0, 0)

    print('\n-- SCALE TEST --')
    assert Point(1, 1).scale(2.0, zero) == (2, 2)
    assert Point(45, 45).scale(0.5, zero) == (22.5, 22.5)

    print('\n-- ROTOZOOM TEST #  1 --')
    print(f'{Point(45, 45).scale(1 / 45, zero).rotate(90, zero).scale(47, zero) == (-47, -47)=}')

    print('\n-- ROTOZOOM TEST #  2 --')
    fifteen = (15, 15)
    print(f'{Point(45, 45).scale(1 / 3, fifteen).rotate(90, fifteen).scale(3, fifteen) == (-15, 45)=}')

    print('\n-- ROTOZOOM TEST #  3 --')
    print(f'{Point(0, 100).rotate(60, zero) == Point(0, 100).rotate(-300, zero)=}')
    print(f'{hash(Point(None, None))=}')
    print(f'{hash(Point(0, 0))=}')
    print(f'{hash(Point(1, 1))=}')


if __name__ == "__main__":
    try:
        run_point_tests()
        print('***************', 'ALL TESTS COMPLETE!', '***************')
    except AssertionError as e:
        print(f'A test, maybe more, failed: {e}')
        print('!!!!   RAN INTO A FEW ERRORS    !!!!')

    # run_point_tests()
    #
    p_scale = Point(5, 5) * 20
    print(f'{p_scale=}')
    p_scale = Point(5, 5) * -10
    print(f'{p_scale=}')
    p_scale = Point(5, 5) * (-10, (1, 1))
    p_scale = Point(5, 5) * ((2, -2), (1, 1))
    p_scale = Point(5, 5) * ((1, 2), (5, 2))
