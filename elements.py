import datetime
import time

from .resources import constants, graphics


class Element:
    """
    Parent class for all `elements`.

    :param: width -> Width of the element (in chars).
    :param: height -> Height of the element (in chars).
    :param: border -> if true the class will draw a border around the element
    """

    def __init__(
        self,
        width: int = 0,
        height: int = 0,
        label: str = '',
        border: bool = False,
        continuous: bool = False,
        right_aligned: bool = False,
        selectable: bool = False,
        linked_element: bool = None):

        self.width = width
        self.height = height
        self.labe = label
        self.border = border
        self.continuous = continuous
        self.right_aligned = right_aligned
        self.selectable = selectable
        self.linked_element = linked_element

        self.nested_elements = None
        self.selected = False

        if self.selectable:
            self.width += 1
        if self.border:
            self.width += 2
            self.height += 2

        print(f'creating pixel array with width: {self.width} and height: {self.height} ...')
        self.pixel_array = [[graphics.BACKGROUND] * self.width for i in range(self.height + 1)]
        print(f'pixel_array: {self.pixel_array}')

    def fill_solid(self, length: int, char: str):
        char_str = ''
        for i in range(length):
            char_str += char
        self.fill(char_str)

    def fill_text(self, text: str):
        x_pos = 0
        y_pos = 0
        x_offset = 0
        y_offset = 0
        if self.border:
            x_offset += 1
            y_offset += 1
        if self.selectable:
            x_pos += 1
        for char in list(text):
            if char == '\n':
                x_pos = 0
                y_pos += 1
            else:
                self.pixel_array[y_pos + y_offset][x_pos + x_offset] = char
                if x_pos < self.width - x_offset:
                    x_pos += 1
                else:
                    if y_pos < self.height - y_offset:
                        y_pos += 1
                        x_pos = 0
                    else:
                        raise Exception('Content size is greater than element size.')

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

    def __init__(self,
        text: str = '',
        width: int = 0,
        height: int = 0,
        label: str = '',
        border: bool = False,
        continuous: bool = False,
        right_aligned: bool = False):

        if text and not width and not height:
            width, height = self.auto_size(text)
            print(f'auto_width:  {width}')
            print(f'auto_height: {height}')

        super().__init__(width, height, label=label, border=border, continuous=continuous, right_aligned=right_aligned)
        self.fill_text(text)

    def auto_size(self, text):
        longest_row = 0
        auto_width = 0
        auto_height = 0
        for char in list(text):
            if char == '\n':
                auto_height += 1
                auto_width = 0
            else:
                auto_width += 1
                longest_row = auto_width if auto_width > longest_row else longest_row
        return (longest_row, auto_height)


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

    def get_elements(self) -> list:
        return self.elements

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
