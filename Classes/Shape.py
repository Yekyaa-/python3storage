from python3storage.Classes.Point import Point


class Shape:
    @staticmethod
    def fix_origin(p_list):
        split_list = list(zip(*[(x, y) for x, y in p_list]))
        avg_x = sum(split_list[0]) / len(split_list[0])
        avg_y = sum(split_list[1]) / len(split_list[1])
        orig = Point(avg_x, avg_y)
        return orig

    def map(self, func):
        """	
        Maps a passed-in function to every Point in the polygon. Changes are immediate.	
        """
        print('map:AFTER:MAP:', self._pt_list)
        for p in self._pt_list:
            result = func(p)
            p[0] = result[0]
            p[1] = result[1]
        print('map:AFTER:MAP:', self._pt_list)

    def get_centroid(self):
        # DEBUG THIS IN SHAPE
        # return self.centroid.round(self.centroid.format_digits_to_round)
        return self.centroid

    def __init__(self, sides=None, radius=None, centroid=None, rot_angle=None, rot_point=None):
        if (sides is not None and type(sides) in (int, float)) or sides is None:
            self.sides = int(sides) or 3
            self.centroid = Point(centroid or (0, 0))
            self.radius = radius or 1.0
            self.rot_point = Point(rot_point or self.centroid)
            self.rot_angle = rot_angle or 0.0
            angle = 360.0 / sides
            # rot_angle = 0

            if type(self.centroid) is not Point:
                assert AssertionError('type(self.centroid) is not Point')
            self._pt_list = [Point(self.centroid + (0, self.radius)).rotate(angle * multiply).rotate(self.rot_angle, self.rot_point) for multiply in
                             range(0, sides)]

        elif type(sides) is Shape:
            obj = sides
            self.sides = obj.sides
            self.radius = obj.radius
            self.centroid = Point(obj.centroid)
            self.rot_angle = obj.rot_angle
            self.rot_point = Point(obj.rot_point)
            self._pt_list = [Point(i) for i in obj]
        elif type(sides) in (list, tuple):
            lst = sides
            self.sides = len(lst)
            self.centroid = Point(centroid if centroid else Shape.fix_origin(lst))
            self.radius = self.centroid.calc_radius(lst[0])
            self.rot_angle = 0
            self.rot_point = self.centroid
            self._pt_list = [Point(i) for i in lst]
        else:
            raise AssertionError(f'{type(sides)=}Only reason sides is not established is here')

    def __init___old(self, sides=None, radius=None, o_pt=None):
        if type(sides) is Shape:
            obj = sides
            self.sides = obj.sides
            self.radius = obj.radius
            if radius and not self.radius:
                self.radius = radius
            self.centroid = obj.get_centroid()
            if o_pt:
                self.translate(o_pt)
                self.centroid = Point(o_pt)
            else:
                self.centroid = Point(0, 0)

            self.radius = self.centroid.calc_radius(obj[0])

            self._pt_list = []
            for pt in obj:
                self._pt_list.append(Point(pt))
            # print(f'------------ COPIED {self} from {obj}')
        elif type(sides) is list:
            self.radius = radius
            self.sides = len(sides)
            self.centroid = Shape.fix_origin(sides)

            self.centroid += o_pt

            self._pt_list = []
            for pt in sides:
                self._pt_list.append(Point(pt))

            if not self.centroid:
                fixed_origin = Shape.fix_origin(self._pt_list)
                print('  &&& Copy Point List, fixed centroid:', self.centroid, ' -> ', fixed_origin)
                self.centroid = fixed_origin
            else:
                print('  &&& Copy Point List, did not fix centroid:', self.centroid)

            if not self.radius or radius < 5:
                cr = self.centroid.calc_radius(self._pt_list[0])
                print('  %.* Calculated Radius to be ', cr, ' not', self.radius)
                self.radius = cr
        else:
            if sides is None or sides <= 2:
                raise ValueError('Shape must be greater than 3 sides.')
            self.sides = sides

            def v_err():
                raise ValueError('Need Radius >= 5')

            self.radius = 2 if radius is None else (radius if radius >= 0.00005 else v_err())

            self.centroid = Point(0, 0) + o_pt
            angle = 360.0 / sides
            print(f'{angle=} {self.sides=} {self.radius=}')
            print(f'{Point(self.centroid[0], self.centroid[1] + 100).rotate(60, self.centroid)=}')

            p_list = [Point(self.centroid[0], self.centroid[1] + self.radius)]

            for s_range in range(0, sides - 1):
                p_list.append(p_list[s_range].rotate(angle, self.centroid))

            self._pt_list = p_list

            if not self.centroid:
                shape_p = Shape.fix_origin(p_list)
                print('  &&& New Shape, fixed centroid     *******:', self.centroid, ' -> ', shape_p)
                self.centroid = shape_p
            else:
                print('  &&& New Shape, did not fix centroid   *:', self.centroid)

    def __len__(self):
        return self.sides

    def __getitem__(self, item):
        # if __name__ == "__main__":
        #     print('Shape.__getitem__:', item, self._pt_list[item])
        #
        return self._pt_list[item]

    def __setitem__(self, item, value):
        # if __name__ == "__main__":
        #     print('Shape.__setitem__:', item, self._pt_list[item], value, end='')
        #
        raise IndexError('Polygon is immutable!')

    def __delitem__(self, key):
        # if __name__ == "__main__":
        #     print('Point.__delitem__:', self, key)
        #
        raise IndexError('Polygon is immutable!')

    def scale(self, factor=1, scale_pt=None):
        if __name__ == "__main__":
            header = f'Shape.   scale   : Shape({self.sides}) {factor=} {scale_pt=}'

        tmp = Shape(self)

        if factor == 1:
            if __name__ == "__main__":
                print(f'{header} returns a copy of self')
            return tmp

        if scale_pt is None:
            scale_pt = self.centroid

        for i in tmp:
            i[0] = i[0] - scale_pt[0]
            i[1] = i[1] - scale_pt[0]

            i[0] = i[0] * factor
            i[1] = i[1] * factor

            i[0] = i[0] + scale_pt[0]
            i[1] = i[1] + scale_pt[1]

        if __name__ == "__main__":
            print(f'{header} == becomes == {tmp}')
        return tmp

    def translate(self, point):
        # if __name__ == "__main__":
        #     print(f'Shape.translate: {self} + {point}')
        #
        x = Shape(self)

        if point is None:
            return x

        for i in x:
            i[0] = i[0] + point[0]
            i[1] = i[1] + point[1]

        x.centroid = (x.centroid + point).round(7)
        # print(f'Shape.translate: {x.centroid}')
        # p_list = []
        # for side_i in range(0, self.sides):
        #     p_list.append(Point(self._pt_list[side_i]) + Point(point))
        # self.set_centroid(Point(self.centroid[0] + point[0], self.centroid[1] + point[1]))
        # self._pt_list = p_list
        return x

    # Rotate the polygon around (ox, oy) with points in polygon respecting self.centroid
    # None will make it spin around it's 'center' or 'centroid'
    # An actual value will rotate all points around that point
    def rotate(self, theta, rot_point=None):
        if __name__ == "__main__":
            print(f'Shape.rotate: Shape({self.sides}) @ ({theta}, {rot_point})')

        if rot_point is None:
            # DEBUG THIS IN SHAPE
            # rot_point = self.centroid.round(self.centroid.format_digits_to_round)
            rot_point = self.centroid

        p_list = []
        for pt in self:
            p_list.append(pt @ (theta, rot_point))

        new_shape = Shape(p_list)
        return new_shape
        # raise AssertionError(str(new_shape))

    def point_list_int(self, offset=None):
        if offset is None:
            offset = self.centroid

        return ((int(var[0] + offset[0]), int(var[1] + offset[1])) for var in self._pt_list)

    def point_list_int_scaled(self, scale=1.0, offset=None):
        if offset is None:
            offset = self.centroid

        return ((int((var[0]) * scale) + offset[0], int((var[1]) * scale) + offset[1]) for var in self._pt_list)

    def _repr_lst(self, format_spec=''):
        string = '['
        lst_len = len(self._pt_list) - 1
        expected = '[' + ', '.join([str(pt) for pt in self._pt_list]) + ']'

        for i, val in enumerate(self._pt_list):
            string += val.__repr__()
            if i < lst_len:
                string += ', '
        string += ']'
        return string

    def _txt_pt_lst(self, format_spec=''):
        return '[' + ', '.join([format(val, format_spec) for val in self._pt_list]) + ']'

    def __str__(self, format_exc=''):
        return f'Shape[V:{self._txt_pt_lst()} E:{self.sides}  R:{round(self.radius, 5)} C:{self.centroid}])'

    def __repr__(self):
        string = f"Shape({self._repr_lst()})"
        return string

    def set_centroid(self, new_origin):
        if type(new_origin) is tuple:
            raise TypeError(f'tuple {self.centroid} tried to escape!1')

        self.centroid = new_origin
        return self

    def __ne__(self, other):
        if __name__ == "__main__":
            header = f'Shape.__ne__:'

        if self.sides != other.sides or len(self) != len(other):
            if __name__ == "__main__":
                print(f'{header} : Base values are different : therefore, they are not equal! True')
            return True

        for i in range(0, len(other)):
            if other[i] in self:
                print(f'{header} : {other[i]} not in self? False')
            else:
                print(f'{header} : {other[i]} not in self! : therefore, they are not equal! True')
                return True

        print(f'{header} : self != other? False')
        return False

    def __eq__(self, other):
        if __name__ == "__main__":
            header = f'Shape.__eq__:'

        if self.sides != other.sides or len(self) != len(other):
            if __name__ == "__main__":
                print(f'{header} : Base values are different : therefore, they are not equal! False')
            return False

        for i in range(0, len(other)):
            if other[i] in self:
                print(f'{header} : {other[i]} in self? : True')
            else:
                print(f'{header} : {other[i]} not in self! : therefore, they are not equal! False')
                return False

        print(f'{header} : self == other? True')
        return True


def run_polygon_tests():
    s, t = test_create_and_compare()
    test_for_loop(s)
    test_rotate(s, t)
    test_sequences(t)
    test_create_from_shape(t)
    triangle = test_triangle_in_equality()

    test_repr_string_equality("Shape([Point(0, 1.0), Point(-0.8660254038, -0.5), Point(0.8660254038, -0.5)])",
                              triangle.__repr__())


def test_triangle_in_equality():
    print('\ntest_triangle_in_equality: Running...')
    triangle = Shape(3)
    triangle_2 = triangle.scale(3)
    assert triangle_2 != triangle
    triangle_2 = Shape(triangle)
    assert triangle_2 == triangle
    print('test_triangle_in_equality: Test successful!')
    return triangle


def test_create_from_shape(t):
    print('\ntest_create_from_shape: Running...')
    g = Shape(t)
    assert g == t
    assert g.translate(Point(15, 15)) != t
    assert g == t
    print('test_create_from_shape: Test successful!')


def test_sequences(t):
    print('\ntest_sequences: Running...')
    print(t[1])
    try:
        del t[2]
    except IndexError as e:
        print('Caught delete error!', e)
    try:
        t[2] = Point(2, 2)
    except IndexError as e:
        print('Caught setitem error!', e)
    print('test_sequences: Test successful!')


def test_create_and_compare():
    print('\ntest_create_and_compare: Running...')
    s = Shape(4)
    t = Shape(4, 100)
    print('t=', t)
    print('s=', s)
    assert str(t) == format(t, '')
    print('test_create_and_compare: Test successful!')
    return s, t


def test_for_loop(s):
    print(f'\ntest_for_loop: Running...')
    # ({s.__repr__()})')
    for index, temp_point in enumerate(s):
        print(f'  :: Point_list[{index}] = {temp_point}')
    print(f'test_for_loop: Test successful!')


def test_repr_string_equality(expected, actual):
    print('\ntest_repr_string_equality: Running...')
    exp_is_longer = len(expected) > len(actual)
    act_is_longer = len(expected) < len(actual)
    same_length = len(expected) == len(actual)
    shortest = expected if same_length or act_is_longer else actual
    longest = expected if exp_is_longer else actual
    lst = [(i, val) for i, val in enumerate(shortest) if longest[i] != shortest[i]]
    if not same_length:
        alen = len(shortest)
        lst += [(i + alen, val) for i, val in enumerate(longest[alen:])]
    act_l = len(actual)
    has_same_length = ", both are same length" if same_length else ""
    has_extra_chars = f", actual has too many chars ({act_l})" if act_is_longer else ""
    has_too_few_chars = f", actual has too few chars ({act_l})" if exp_is_longer else ""
    both_same = ", both are the exact same" if same_length and len(lst) < 1 else ", difference"
    multi = "s" if len(lst) > 1 else ""
    string = f'Expected \'{expected}\'{has_same_length}{has_extra_chars}{has_too_few_chars}{both_same}{multi} at {lst}'
    print(string)
    print(actual)
    print(expected)

    assert actual == expected, string
    print('test_repr_string_equality: Test successful!')


def test_rotate(s, t):
    print('\ntest_rotate: Running...')
    _ = s.rotate(20, s.centroid)
    _ = s.rotate(40, s.centroid)
    z = s.rotate(90, s.centroid)
    print('test_rotate:         Original s :', s)
    print('test_rotate: Copy of Original s :', t)
    print('test_rotate: Rot 60  Original s :', z)
    assert t != z and z == s, 't should not equal z and z should be equal to s'
    print('test_rotate: Test successful!')


if __name__ == "__main__":
    # test_rotate(Shape(4), Shape(4, 100))
    run_polygon_tests()
    print('***************', 'ALL TESTS COMPLETE!', '***************')
