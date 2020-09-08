import math

from python3storage.Classes.Point import Point

zoom_factor = 1.0


def new_translate_to_world(screen_pt=None, zoom_pt=None, zoom_f=1.0):
    """
    This is going to be the replacement for translate_to_world
    Args:
        screen_pt: Value to convert to screen coordinates
        zoom_pt: The center of the zooming (can be origin, or mouse position)
        zoom_f: Zoom factor. if z > 1: zoom_in elif z < 1: zoom_out else: nothing

    Returns:
        Translated point in world coordinates
    """
    if screen_pt is None:
        raise ValueError(f'Cannot translate None point to world co-ords')

    if zoom_pt is None:
        assert zoom_pt is not None, f'{zoom_pt=}, {screen_pt=}'
    #
    # if zoom_f == 1.0:
    #     return Point(world_pt)

    # This is the calculation from to_screen, reverse it to get to_world
    # new_x = (screen_pt[0] - zoom_pt[0]) * zoom_f + zoom_pt[0]
    new_x = (screen_pt[0] - zoom_pt[0]) / zoom_f + zoom_pt[0]

    # When do I flip the screen on Y?
    # new_y = -((world_pt[1] - zoom_pt[1]) * zoom_f + zoom_pt[1])
    # This is the calculation from to_screen, reverse it to get to_world
    # new_y = (screen_pt[1] - zoom_pt[1]) * zoom_f + zoom_pt[1]
    new_y = (screen_pt[1] - zoom_pt[1]) / zoom_f + zoom_pt[1]
    ret_val = Point(new_x, new_y)
    # print(f':  scale {world_pt: 7.2f} by {zoom_f:1.1f} @ {zoom_pt: 7.2f} as zoom center : Result : {ret_val:7.2f}')
    # string = f'{ret_val:7.2f}'
    return ret_val


def new_translate_to_gui_screen(world_pt=None, zoom_pt=None, zoom_f=1.0):
    """
    This is going to be the replacement for translate_to_screen
    Args:
        world_pt: Value to convert to screen coordinates
        zoom_pt: The center of the zooming (can be origin, or mouse position)
        zoom_f: Zoom factor. if z > 1: zoom_in elif z < 1: zoom_out else: nothing

    Returns:
        Translated Point in screen coordinates
    """
    if world_pt is None:
        raise ValueError(f'Cannot translate None point to screen co-ords')

    if zoom_pt is None:
        assert zoom_pt is not None, f'{zoom_pt=}, {world_pt=}'
    #
    # if zoom_f == 1.0:
    #     return Point(world_pt)

    new_x = (world_pt[0] - zoom_pt[0]) * zoom_f + zoom_pt[0]
    # new_y = -((world_pt[1] - zoom_pt[1]) * zoom_f + zoom_pt[1])
    new_y = (world_pt[1] - zoom_pt[1]) * zoom_f + zoom_pt[1]
    ret_val = Point(new_x, new_y)
    # print(f':  scale {world_pt: 7.2f} by {zoom_f:1.1f} @ {zoom_pt: 7.2f} as zoom center : Result : {ret_val:7.2f}')
    # string = f'{ret_val:7.2f}'
    return ret_val


def run_translate_tests(pt_lst=None, pt_lst_ans=None, zoom_point=None, scale_factor=None):
    if pt_lst is None:
        pt_lst = [Point(450, 225), Point(450, 325), Point(350, 325), Point(250, 425)]

    if pt_lst_ans is None:
        pt_lst_ans = [[[Point(400, 275), Point(400, 325), Point(350, 325), Point(300, 375)],
                       [Point(350, 325), Point(350, 375), Point(300, 375), Point(250, 425)],
                       [Point(225, 112.50), Point(225, 162.5), Point(175, 162.5), Point(125, 212.5)]],

                      [[Point(450, 225), Point(450, 325), Point(350, 325), Point(250, 425)],
                       [Point(450, 225), Point(450, 325), Point(350, 325), Point(250, 425)],
                       [Point(450, 225), Point(450, 325), Point(350, 325), Point(250, 425)]],

                      [[Point(550, 125), Point(550, 325), Point(350, 325), Point(150, 525)],
                       [Point(650, 25), Point(650, 225), Point(450, 225), Point(250, 425)],
                       [Point(900, 450), Point(900, 650), Point(700, 650), Point(500, 850)]],

                      [[Point(600, 75), Point(600, 325), Point(350, 325), Point(100, 575)],
                       [Point(750, -75), Point(750, 175), Point(500, 175), Point(250, 425)],
                       [Point(1125, 562.50), Point(1125, 812.5), Point(875, 812.5), Point(625, 1062.5)]]
                      ]
    if zoom_point is None:
        zoom_point = [Point(350, 325), Point(250, 425), Point(0, 0)]

    if scale_factor is None:
        scale_factor = [0.5, 1.0, 2.0, 2.5]

    expected_test_count = len(scale_factor) * len(zoom_point) * len(pt_lst)
    test_count = 0

    print(f'\nTesting Point(s)\n  {pt_lst}\n with Zoom(s)\n  {zoom_point}\n with Scale(s)\n  {scale_factor}')
    print('-' * 100)

    for s_index, s_factor in enumerate(scale_factor):
        for z_index, z_pt in enumerate(zoom_point):
            for p_index, pt_to_check in enumerate(pt_lst):
                expected = format(pt_lst_ans[s_index][z_index][p_index], '7.2f')
                ret_value = new_translate_to_gui_screen(pt_to_check, z_pt, s_factor)
                result = format(ret_value, '7.2f')
                msg = f'world_to_gui(Point{pt_to_check}, Point{z_pt}, {s_factor}) == {expected}?'
                errmsg = msg + f' *** FALSE, got ...{result}...'

                readable = f'{pt_to_check: 7.2f} * ({s_factor: 7.2f}, Point{z_pt: 7.2f}) == {expected}? TRUE!'
                try:
                    assert result == expected, errmsg
                    test_count += 1
                    # print(msg + ' YES! -> ' + result)
                    print(readable)
                except AssertionError as e:
                    print(e)
                    return test_count, expected_test_count

                try:
                    world = format(new_translate_to_world(ret_value, z_pt, s_factor), '7.2f')
                    screen_pt = format(pt_to_check, '7.2f')
                    assert world == screen_pt, f'{ret_value} * ({s_factor}, {z_pt}) :: {world} != {screen_pt}'
                except AssertionError as e:
                    print(e)
                    return test_count, expected_test_count

    return test_count, expected_test_count


def run_second_test_suite():
    pa = [[[Point(10, 10), Point(30, 10), Point(30, 30), Point(-10, -10)],
           [Point(0, 0), Point(20, 0), Point(20, 20), Point(-20, -20)]],
          [[Point(0, 0), Point(10, 0), Point(10, 10), Point(-10, -10)],
           [Point(0, 0), Point(10, 0), Point(10, 10), Point(-10, -10)]]
          ]
    pl = [Point(0, 0), Point(10, 0), Point(10, 10), Point(-10, -10)]
    z = [Point(-10, -10), Point(0, 0)]
    s = [2.0]

    return run_translate_tests(pt_lst=pl, scale_factor=s, pt_lst_ans=pa, zoom_point=z)


def run_hand_checked_test_suite():
    pa = [[[Point(-25, -25), Point(25, 25), Point(50, 50), Point(75, 75), Point(125, 125)]],
          [[Point(-12.5, -12.5), Point(25, 25), Point(43.75, 43.75), Point(62.5, 62.5), Point(100, 100)]]
          ]
    pl = [Point(0, 0), Point(25, 25), Point(37.5, 37.5), Point(50, 50), Point(75, 75)]
    z = [Point(25, 25)]
    s = [2.0, 1.5]

    return run_translate_tests(pt_lst=pl, scale_factor=s, pt_lst_ans=pa, zoom_point=z)


def t2s(world_point, screen_origin=Point(350, 325)):
    world_point = Point(world_point)
    # print(f't2s-------{world_point=}')
    # Use existing axes_origin to get screen points to correct world point
    origin = Point(0, 0)

    scale_x = 10
    ' Pixels per unit (integer tick size) f\'{scale_x}\' means 0.0 to 1.0 is 0.1 Pixels, '
    # Should I do this for "flipped" coordinates?
    scale_y = -10
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
    return transformed_point


def t2w(screen_point, origin=Point(0, 0), screen_origin=Point(350, 325)):
    screen_point = Point(screen_point)
    # print(f't2w-------{screen_point=}')

    # Use existing axes_origin to get screen points to correct world point

    scale_x = 0.1
    # Should I do this for "flipped" coordinates?
    scale_y = -0.1
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
    return transformed_point


def run_t2w_tests(screen_pt=None, zoom_pt=None, zoom_f=1.0):
    # Other translations are fine, but I need to go from
    # traditional Euclidean 2-D space to a GUI screen
    # Take "Mouse Pos" in screen coords and translate
    # to world coordinates as if you were looking at a sheet
    # of paper.
    s_pt = [Point(350, 325), Point(450, 225), Point(450, 325)]
    o_pt = [Point(0, 0)]
    w_expected = [Point(0, 0), Point(10, 10), Point(10, 0)]

    for s_index, screen_point in enumerate(s_pt):
        p = screen_point
        w = t2w(p)
        s = t2s(w)
        print(f'{p} -> t2w(p)={w} -> f{w_expected[s_index]=} {p} == {s}? {p == s}')
    return


def t2wf(point, axes_origin=None, oldscale=10):
    if axes_origin is None:
        axes_origin = Point(350, 325)
    return scale(point - axes_origin, 1 / oldscale)


def scale(point, scale, m_pt = None):
    if m_pt is None:
        m_pt = (400, 275)

    return Point((point[0] - m_pt[0]) * scale, (point[1] - m_pt[1]) * -scale)


def top(point, zoom_pt, scale_factor):
    def top_scale(point, scale_factor):
        return Point(point[0] * scale_factor, point[1] * -scale_factor)

    translated = point - zoom_pt
    print(f'{translated=}')
    scaled = top_scale(translated, scale_factor)
    print(f'{scaled=}')
    final = scaled

    return final


def formula(point, zmp, newscale=20, oldscale=10):
    def apply_scale(point, scale):
        return  Point(point[0] * scale, point[1] * scale)

    if zmp is None:
        zmp = Point(400, 275)

    change_in_scale = newscale / oldscale
    value = zmp - apply_scale(zmp - point, change_in_scale)
    print(f'{point} -> {value}')
    return value


def run_translate_around_mouse_tests():
    # point_list = [Point(350, 325), Point(400, 275), Point(450, 225), Point(450, 325), Point(250, 425)]
    # point_list = [Point(0, 0), Point(5, 5), Point(10, 10), Point(10, 0), Point(-10, -10)]
    # expected_values = [Point(300, 375), Point(400, 275), Point(500, 175), Point(500, 375), Point(100, 575)]
    point_list = [Point(350, 325), Point(400, 275), Point(450, 225), Point(450, 325), Point(250, 425)]
    expected_values = [Point(300, 375), Point(400, 275), Point(500, 175), Point(500, 375), Point(100, 575)]
    zoom_pt = (400, 275)
    result = formula(Point(0, 0), zmp=zoom_pt)
    print(result, result, result)
    e = len(expected_values)
    t = 0
    for i, pt in enumerate(point_list):
        try:
            result = formula(pt, zmp=zoom_pt)
            assert result == expected_values[i], f'failed {i+1}: Expected {expected_values[i]}, got {result}'
            print(f'PASSED {i+1}: Expected {expected_values[i]}, got {result}')
            t += 1
        except AssertionError as err:
            print(err)
    return t, e


if __name__ == "__main__":
    # t, e = run_translate_tests()
    # print(f'****** {t} / {e} TESTS PASSED ******')
    #
    # t, e = run_second_test_suite()
    # print(f'****** {t} / {e} TESTS PASSED ******')
    #
    # t, e = run_hand_checked_test_suite()
    # print(f'****** {t} / {e} TESTS PASSED ******')
    #
    # run_t2w_tests()
    t, e = run_translate_around_mouse_tests()
    print(f'****** {t} / {e} TESTS PASSED ******')