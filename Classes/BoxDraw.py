# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 08:33:26 2020

@author: M70308
"""

import argparse


class BoxDrawer:
    def __init__(self, width, height, vsplit=[], hsplit=[], characterSet=1):
        self.fcList = ((self.isTopLeft, '\u250C', 'o'),
                       (self.isTopRight, '\u2510', 'o'),
                       (self.isBotLeft, '\u2514', 'o'),
                       (self.isBotRight, '\u2518', 'o'),
                       (self.isConnect_1111, '\u253C', '+'),
                       (self.isConnect_0111, '\u252C', '+'),
                       (self.isConnect_1011, '\u2524', '+'),
                       (self.isConnect_1101, '\u2534', '+'),
                       (self.isConnect_1110, '\u251C', '+'),
                       (self.isConnect_1010, '\u2502', '|'),
                       (self.isConnect_0101, '\u2500', '-'),
                       (self.isXEdge, '\u2502', 'I'),
                       (self.isYEdge, '\u2500', '=')
                       )

        if width is None:
            width = 100
        if height is None:
            height = 25
        self.cs = characterSet
        self.x = 0
        self.y = 0
        self.height = height
        self.width = width
        self.lastx = self.width - self.x - 1
        self.lasty = self.height - self.y - 1
        self.vsplit = []
        self.hsplit = []
        if vsplit is not None:
            for v in vsplit:
                self.addVSplit(v, 0)
        if hsplit is not None:
            for h in hsplit:
                self.addHSplit(0, h)

    @property
    def hRange(self):
        return range(self.x, self.width)

    @property
    def vRange(self):
        return range(self.y, self.height)

    def point_as_char(self, x, y):
        for func, charset1, charset2 in self.fcList:
            if func(x, y):
                if self.cs == 1:
                    return charset1
                elif self.cs == 2:
                    return charset2

        return None

    def __str__(self):
        return (f"({self.x}, {self.y}, {self.lastx}, {self.lasty}) " +
                f"SplitH={self.hsplit} SplitV={self.vsplit} - CS:{self.cs}")

    def isConnect_0111(self, x, y):
        '''
        Is this point a connection to three points (xRDL)?
        '''
        return x in self.vsplit and y == self.y

    def isConnect_1011(self, x, y):
        '''
        Is this point a connection to three points (UxDL)?
        '''
        return y in self.hsplit and x == self.lastx

    def isConnect_1101(self, x, y):
        '''
        Is this point a connection to three points (URxL)?
        '''
        return x in self.vsplit and y == self.lasty

    def isConnect_1110(self, x, y):
        '''
        Is this point a connection to three points (URDx)?
        '''
        return y in self.hsplit and x == self.x

    def isConnect_1111(self, x, y):
        '''
        Is this point a connection to all four points around it?
        '''
        return self.isConnect_1010(x, y) and self.isConnect_0101(x, y)

    def isConnect_1010(self, x, y):
        '''
        Is this point a connection to Above and Below, but not an L/R Edge?
        '''
        return x in self.vsplit and not self.isXEdge(x, y)

    def isConnect_0101(self, x, y):
        '''
        Is this point a connection to Left and Right, but not an U/D Edge?
        '''
        return y in self.hsplit and not self.isYEdge(x, y)

    def isXEdge(self, x, y):
        '''
        Is this point on the Left or Right edge?
        '''
        return x in [self.x, self.lastx]

    def isYEdge(self, x, y):
        '''
        Is this point on the Top or Bottom edge?
        '''
        return y in [self.y, self.lasty]

    def isTopLeft(self, x, y):
        return (x, y) == (self.x, self.y)

    def isTopRight(self, x, y):
        return (x, y) == (self.lastx, self.y)

    def isBotLeft(self, x, y):
        return (x, y) == (self.x, self.lasty)

    def isBotRight(self, x, y):
        return (x, y) == (self.lastx, self.lasty)

    def isHSplit(self, x, y):
        '''
        Is this point in the horizontal splitter list?
        '''
        return y in self.hsplit

    def isVSplit(self, x, y):
        '''
        Is this point in the vertical splitter list?
        '''
        return x in self.vsplit

    def addHSplit(self, x, y):
        '''
        Add a horizontal splitter at row y
        '''
        if y not in self.hsplit + [self.y, self.lasty]:
            if y in range(self.y, self.height):
                self.hsplit += [y]

    def addVSplit(self, x, y):
        '''
        Add a vertical splitter at column x
        '''
        if x not in self.vsplit + [self.x, self.lastx]:
            if x in range(self.x, self.width):
                self.vsplit += [x]

    def box_text_zip_or_mask(self, text_array=None, box_array=None):
        if text_array is None:
            print(text_array, ' is None (txt_array)')
        if box_array is None:
            print(box_array, ' is None (box_array)')
        result_string = ''
        box_array = self.as_string().splitlines()

        result_string += text_array
        return result_string

    def as_string(self, indent=0, message=None):
        '''
        Draw the box with the currently defined parameters.
        '''
        return_string_value = ''
        indenter = ' ' * indent
        skip_message = False if message else True
        ch = None

        x_txt_counter = 0
        y_txt_counter = 0

        if not skip_message:
            # Separate each line, removing end-of-line returns
            message = message.splitlines(False) if message else ''

            msg_len = len(message)

            msg_len_y = 0

        for y in self.vRange:
            return_string_value += indenter

            if not skip_message and msg_len:

                try:
                    if y_txt_counter < msg_len:
                        msg_len_y = len(message[y_txt_counter])
                except:
                    assert False, f'{x_txt_counter=} {y_txt_counter=} {list(message)=} ch=\'{ch}\' {msg_len=} {msg_len_y=}'

            # For the range(self.x, self.width - self.x + 1)
            for x in self.hRange:
                ch = self.point_as_char(x, y)
                if ch is not None:
                    return_string_value += ch
                else:
                    if skip_message or x_txt_counter >= msg_len_y or y_txt_counter >= msg_len:
                        return_string_value += ' '
                    else:
                        # print(f'{x_txt_counter=} {y_txt_counter=} {list(message)=} ch=\'{ch}\' {msg_len=} {msg_len_y=}')
                        m_char = message[y_txt_counter][x_txt_counter]
                        # print(f'assign \'{m_char}\'')
                        return_string_value += m_char
                        x_txt_counter += 1
                # else:
                #     assert False, f'{x_txt_counter=} {y_txt_counter=} {list(message)=} ch=\'{ch}\' {msg_len=} {msg_len_y=}'

            # if y is not 0
            if y:
                x_txt_counter = 0
                y_txt_counter += 1

            # Print line number at the end (solve spacing issues)
            return_string_value += '\n'

        return return_string_value


class Box:
    def __init__(self, width, height, vsplit=[], hsplit=[], characterSet=1):
        self.fcList = ((self.isTopLeft, '\u250C', 'o'),
                       (self.isTopRight, '\u2510', 'o'),
                       (self.isBotLeft, '\u2514', 'o'),
                       (self.isBotRight, '\u2518', 'o'),
                       (self.isConnect_1111, '\u253C', '+'),
                       (self.isConnect_0111, '\u252C', '+'),
                       (self.isConnect_1011, '\u2524', '+'),
                       (self.isConnect_1101, '\u2534', '+'),
                       (self.isConnect_1110, '\u251C', '+'),
                       (self.isConnect_1010, '\u2502', '|'),
                       (self.isConnect_0101, '\u2500', '-'),
                       (self.isXEdge, '\u2502', 'I'),
                       (self.isYEdge, '\u2500', '=')
                       )

        if width is None:
            width = 100
        if height is None:
            height = 25
        self.cs = characterSet
        self.x = 0
        self.y = 0
        self.height = height
        self.width = width
        self.lastx = self.width - self.x - 1
        self.lasty = self.height - self.y - 1
        self.vsplit = []
        self.hsplit = []
        if vsplit is not None:
            for v in vsplit:
                self.addVSplit(v, 0)
        if hsplit is not None:
            for h in hsplit:
                self.addHSplit(0, h)

    @property
    def hRange(self):
        return range(self.x, self.width)

    @property
    def vRange(self):
        return range(self.y, self.height)

    def point_as_char(self, x, y):
        for func, charset1, charset2 in self.fcList:
            if func(x, y):
                if self.cs == 1:
                    return charset1
                elif self.cs == 2:
                    return charset2

        return ' '

    def __str__(self):
        return (f"({self.x}, {self.y}, {self.lastx}, {self.lasty}) " +
                f"SplitH={self.hsplit} SplitV={self.vsplit} - CS:{self.cs}")

    def isConnect_0111(self, x, y):
        '''
        Is this point a connection to three points (xRDL)?
        '''
        return x in self.vsplit and y == self.y

    def isConnect_1011(self, x, y):
        '''
        Is this point a connection to three points (UxDL)?
        '''
        return y in self.hsplit and x == self.lastx

    def isConnect_1101(self, x, y):
        '''
        Is this point a connection to three points (URxL)?
        '''
        return x in self.vsplit and y == self.lasty

    def isConnect_1110(self, x, y):
        '''
        Is this point a connection to three points (URDx)?
        '''
        return y in self.hsplit and x == self.x

    def isConnect_1111(self, x, y):
        '''
        Is this point a connection to all four points around it?
        '''
        return self.isConnect_1010(x, y) and self.isConnect_0101(x, y)

    def isConnect_1010(self, x, y):
        '''
        Is this point a connection to Above and Below, but not an L/R Edge?
        '''
        return x in self.vsplit and not self.isXEdge(x, y)

    def isConnect_0101(self, x, y):
        '''
        Is this point a connection to Left and Right, but not an U/D Edge?
        '''
        return y in self.hsplit and not self.isYEdge(x, y)

    def isXEdge(self, x, y):
        '''
        Is this point on the Left or Right edge?
        '''
        return x in [self.x, self.lastx]

    def isYEdge(self, x, y):
        '''
        Is this point on the Top or Bottom edge?
        '''
        return y in [self.y, self.lasty]

    def isTopLeft(self, x, y):
        return (x, y) == (self.x, self.y)

    def isTopRight(self, x, y):
        return (x, y) == (self.lastx, self.y)

    def isBotLeft(self, x, y):
        return (x, y) == (self.x, self.lasty)

    def isBotRight(self, x, y):
        return (x, y) == (self.lastx, self.lasty)

    def isHSplit(self, x, y):
        '''
        Is this point in the horizontal splitter list?
        '''
        return y in self.hsplit

    def isVSplit(self, x, y):
        '''
        Is this point in the vertical splitter list?
        '''
        return x in self.vsplit

    def addHSplit(self, x, y):
        '''
        Add a horizontal splitter at row y
        '''
        if y not in self.hsplit + [self.y, self.lasty]:
            if y in range(self.y, self.height):
                self.hsplit += [y]

    def addVSplit(self, x, y):
        '''
        Add a vertical splitter at column x
        '''
        if x not in self.vsplit + [self.x, self.lastx]:
            if x in range(self.x, self.width):
                self.vsplit += [x]

    def as_string(self, indent=0, message=None):
        '''
        Draw the box with the currently defined parameters.
        '''
        return_string_value = ''
        indenter = ' ' * indent
        # For the range(self.x, self.width - self.x + 1)
        for y in self.vRange:
            return_string_value += indenter
            # For the range(self.x, self.width - self.x + 1)
            for x in self.hRange:
                return_string_value += self.point_as_char(x, y)
            # Print line number at the end (solve spacing issues)
            return_string_value += '\n'

        return return_string_value


def draw(box, blank=' '):
    '''
    Draw the box with the currently defined parameters.
    '''
    print(f"{str(box):^{box.width}}")
    print(displayNumbersHorizontal(box.width, blank), end='')

    j = 0
    split_line = box.as_string().splitlines()
    print(split_line)
    print(list(box.as_string('message\nmessage 2')))
    split_line_count = len(split_line)
    number_size = len(str(split_line_count - 1))

    for i in split_line:
        if blank != ' ':
            print(f'{i} {j:{blank}{number_size}}')
        else:
            print(f'{i} {j:>{number_size}}')
        j += 1
    # print(self.draw_as_string(), end='')


def displayNumbersHorizontal(number=None, blank=' ', indent=0):
    '''
    Print a horizontal bar using one column per number, one line per digit
    such that calling self.hDisplay(71) prints the following:
    00000000001111111111222222222233333333334444444444555555555566666666667
    01234567890123456789012345678901234567890123456789012345678901234567890
    '''

    # Default value of number is box width
    if number is None:
        return ''

    # Setup indenting
    indent_spaces = ' ' * indent

    # Establish length of number as string
    string_length_value = len(str(number - 1))

    # Setup return value
    return_value = ''

    # Do digits in order as powers of 10 (10**3, 10**2, 10**1)
    for digit_index in range(string_length_value - 1, -1, -1):
        # Add optional indenting
        return_value += indent_spaces

        # for each line, display 0 - digit for width characters
        for column_counter in range(0, number):
            # 0 // 10^0 = 100 % 10 = 0
            this_digit = (column_counter // (10 ** digit_index)) % 10

            print_digit = str(this_digit)
            if digit_index != 0 and this_digit == 0:
                print_digit = str(blank)
            return_value += print_digit

        return_value += '\n'

    return return_value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Display a Box',
                                     allow_abbrev=False)

    parser.add_argument('-w', metavar='W',
                        dest='width', type=int, nargs='?',
                        default=100, required=False,
                        help='Width of the Box')

    parser.add_argument('-ht', metavar='H',
                        dest='height', type=int, nargs='?',
                        default=25, required=False,
                        help='Height of the Box')

    parser.add_argument('-sh', '--split-horizontal', metavar='N',
                        action='store', type=int,
                        nargs='+', default=[],
                        help='Horizontal Splitters')

    parser.add_argument('-sv', '--split-vertical', metavar='N',
                        action='store', type=int,
                        nargs='+', default=[],
                        help='Vertical Splitters')

    parser.add_argument('-cs', '--character-set', metavar='N', type=int,
                        action='store', choices=(1, 2), default=1,
                        help='Character Set 1 or 2')

    args = parser.parse_args()

    # print(vars(args))
    hsplit = []
    if 'split_horizontal' in vars(args) and args.split_horizontal != []:
        hsplit = args.split_horizontal
    else:
        for j in range(0, args.height):
            if not (j % (args.height // 4)):
                hsplit += [j]

    vsplit = []
    if 'split_vertical' in vars(args) and args.split_vertical != []:
        vsplit += args.split_vertical
    else:
        for i in range(0, args.width):
            if not (i % (args.width // 4)):
                vsplit += [i]

    b = Box(args.width, args.height, vsplit, hsplit, args.character_set)

    # draw(b)

    c = BoxDrawer(10, 10, hsplit=[3])
    print(c.as_string())

    print(c.as_string(message='Test\n1\n\n2\n3'))
