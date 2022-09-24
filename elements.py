import datetime
import time

from .resources import constants, graphics
from .custom_exceptions import ElementOverflow, InvalidElement


class Element:
    """
    Parent class for all `elements`.

    :param: width -> Width of the element (in chars).
    :param: height -> Height of the element (in chars).
    :param: border -> if true the class will draw a border around the element
    """

    def __init__(self, width: int = 0, height: int = 0, border: bool = False, continuous: bool = False,
                 right_aligned: bool = False, selectable: bool = False, linked_element: bool = None):
        self.width = width
        self.height = height
        self.border = border
        self.continuous = continuous
        self.right_aligned = right_aligned
        self.selectable = selectable
        self.linked_element = linked_element

        self.selected = False

        if self.selectable:
            self.width += 1
        if self.border:
            self.width += 2
            self.height += 2

        self.pixel_array = [[graphics.BACKGROUND] * width for i in range(height)]

    def fill_solid(self, length: int, char: str):
        char_str = ''
        for i in range(length):
            char_str += char
        self.fill(char_str)

    def fill(self, text: str):
        char_list = list(text)
        x_pos = 0
        y_pos = 0
        x_offset = 0
        y_offset = 0
        if self.border:
            x_offset += 1
            y_offset += 1
        if self.selectable:
            x_offset += 1

        for char in char_list:
            if char == '\n':
                x_pos = 0
                y_pos += 1
            else:
                self.pixel_array[y_pos + y_offset][x_pos + x_offset] = char
                x_pos = x_pos + 1 if x_pos < self.width - x_offset else 0
                y_pos = y_pos + 1 if x_pos >= self.width - x_offset else y_pos
            if y_pos >= self.height - y_offset:
                raise InvalidElement('Content size is greater than element size.')

    def select(self):
        if self.selectable:
            self.selected = True
            if self.border:
                self.pixel_array[1][1] = graphics.CURSOR
            else:
                self.pixel_array[0][0] = graphics.CURSOR

    def deselect(self):
        if self.selectable:
            self.selected = False
            if self.border:
                self.pixel_array[1][1] = graphics.BACKGROUND
            else:
                self.pixel_array[0][0] = graphics.BACKGROUND

    def act(self):
        pass
        # TODO: log NotImplemented() or something

    def link_element(self, element):
        self.linked_element = element


class NoneElement(Element):
    """
    Placeholder element with no content.
    """

    def __init__(self):
        super().__init__()


class Line(Element):
    """
    Horizontal line spanning the full width of the page.
    """

    def __init__(self):
        super().__init__(constants.MAX_SCREEN_WIDTH, 1)
        self.fill_solid(constants.MAX_SCREEN_WIDTH, graphics.LINE)


class Text(Element):
    """
    Element that holds text. Use optional parameters `width` and/or `height` to specify a fixed-length or multi-line
    Text element.
    """

    def __init__(self, text: str, width: int, height: int, border=False, continuous=False, right_aligned=False):
        super().__init__(width + 2, 3, continuous=continuous, right_aligned=right_aligned, selectable=selectable)


class TextInput(Element):
    """
    Input field, that when active, allows the user to enter text via keyboard.
    """

    def __init__(self, length: int, continuous=False, right_aligned=False):
        super().__init__(length + 1, 1, continuous=continuous, right_aligned=right_aligned)
        self.active = False
        self.text_length = length
        self.text = ''
        self.last_blink = time.perf_counter()
        self.cursor_location = 0
        for i in range(self.text_length):
            self.pixel_array[0][i] = graphics.TEXT_BACKGROUND

    def act(self):
        if self.active:
            self.active = False
            if self.cursor_location == self.text_length:
                self.pixel_array[0][self.cursor_location] = graphics.BACKGROUND
            else:
                self.pixel_array[0][self.cursor_location] = graphics.TEXT_BACKGROUND
            return 'inactive'
        else:
            self.active = True
            return 'active'

    def add_char(self, character: str):
        if self.cursor_location < self.text_length:
            self.pixel_array[0][self.cursor_location] = character
            self.text += character
            self.cursor_location += 1

    def remove_char(self):
        if self.cursor_location > 0:
            if self.cursor_location == self.text_length:
                self.pixel_array[0][self.cursor_location] = graphics.BACKGROUND
                self.pixel_array[0][self.cursor_location - 1] = graphics.TEXT_BACKGROUND
            else:
                self.pixel_array[0][self.cursor_location] = graphics.TEXT_BACKGROUND
                self.pixel_array[0][self.cursor_location - 1] = graphics.TEXT_BACKGROUND
            self.cursor_location -= 1
            self.text = self.text[0:self.cursor_location]

    def monitor(self):
        if self.active:
            if time.perf_counter() > self.last_blink + constants.CURSOR_BLINK_INTERVAL:
                self.last_blink = time.perf_counter()
                if self.pixel_array[0][self.cursor_location] == graphics.TEXT_CURSOR:
                    if self.cursor_location == self.text_length:
                        self.pixel_array[0][self.cursor_location] = graphics.BACKGROUND
                    else:
                        self.pixel_array[0][self.cursor_location] = graphics.TEXT_BACKGROUND
                else:
                    self.pixel_array[0][self.cursor_location] = graphics.TEXT_CURSOR


class ElementCollection:
    """
    """

    def __init__(self):
        self.elements = []
        self.select_locked = False
        self.selected_element = None
        self.selected_position = None

    def add_element(self, element: Element, position: int = -1):
        if position < 0:
            self.elements.append(element)
        else:
            self.elements.insert(position, Element)

    def select_next(self):
        pass

    def select_previous(self):
        pass


def build_border(pixel_array: list):
    width = len(pixel_array[0])
    height = len(pixel_array)
    for row in range(height):
        for col in range(width):
            # Check for corners
            if row == 0 and col == 0:
                pixel_array[row][col] = graphics.CORNER_TOP_LEFT
            elif row == 0 and col == width - 1:
                pixel_array[row][col] = graphics.CORNER_TOP_RIGHT
            elif row == height - 1 and col == 0:
                pixel_array[row][col] = graphics.CORNER_BOTTOM_LEFT
            elif row == height - 1 and col == width - 1:
                pixel_array[row][col] = graphics.CORNER_BOTTOM_RIGHT
            # Check for edges
            elif row == 0:
                pixel_array[row][col] = graphics.EDGE_TOP
            elif row == height - 1:
                pixel_array[row][col] = graphics.EDGE_BOTTOM
            elif col == 0:
                pixel_array[row][col] = graphics.EDGE_LEFT
            elif col == width - 1:
                pixel_array[row][col] = graphics.EDGE_RIGHT
    return pixel_array
