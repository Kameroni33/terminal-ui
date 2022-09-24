import os
import cursor

from .resources import constants, graphics
from .pages import PageCollection


class Display:

    def __init__(self, page_collection: PageCollection):
        self.pages = page_collection

        self.width = None
        self.height = None
        self.canvas = None
        self._refresh = False

        self.scroll_vertical = 0
        self.scroll_horizontal = 0

        os.system('cls' if os.name == 'nt' else 'clear')
        cursor.hide()

    def clear(self):
        if self._refresh:
            os.system('cls' if os.name == 'nt' else 'clear')
            self._refresh = False
        else:
            print(f'\033[H', end='')

    def refresh(self):
        self._refresh = True

    def scroll_down(self):
        self.scroll_vertical += constants.SCROLL_AMOUNT

    def scroll_up(self):
        if self.scroll_vertical > 0:
            self.scroll_vertical -= constants.SCROLL_AMOUNT

    def scroll_right(self):
        self.scroll_horizontal += constants.SCROLL_AMOUNT

    def scroll_left(self):
        if self.scroll_horizontal > 0:
            self.scroll_horizontal -= constants.SCROLL_AMOUNT

    def scroll_home(self):
        self.scroll_vertical = 0
        self.scroll_horizontal = 0

    def update_screen_size(self):
        self.width = os.get_terminal_size()[0]
        self.height = os.get_terminal_size()[1]
        # For debugging purposes
        # self.width = 120
        # self.height = 30
        self.canvas = [[graphics.BACKGROUND] * self.width for i in range(self.height)]

    def render_border(self):
        for row in range(self.height):
            for col in range(self.width):
                # Check for corners
                if row == 0 and col == 0:
                    self.canvas[row][col] = graphics.CORNER_TOP_LEFT
                elif row == 0 and col == self.width-1:
                    self.canvas[row][col] = graphics.CORNER_TOP_RIGHT
                elif row == self.height-1 and col == 0:
                    self.canvas[row][col] = graphics.CORNER_BOTTOM_LEFT
                elif row == self.height-1 and col == self.width-1:
                    self.canvas[row][col] = graphics.CORNER_BOTTOM_RIGHT
                # Check for edges
                elif row == 0:
                    self.canvas[row][col] = graphics.EDGE_TOP
                elif row == self.height-1:
                    self.canvas[row][col] = graphics.EDGE_BOTTOM
                elif col == 0:
                    self.canvas[row][col] = graphics.EDGE_LEFT
                elif col == self.width-1:
                    self.canvas[row][col] = graphics.EDGE_RIGHT

    def render_elements(self, canvas_row_start: int, canvas_row_stop: int, canvas_col_start: int, canvas_col_stop: int, elements: list):
        canvas_row_pos = canvas_row_start
        canvas_col_pos = canvas_col_start
        for element in elements:
            if element.nested_elements:
                raise Exception('nested elements are not yet supported')
            else:
                printing_current_element = True
                element_row_pos = 0
                element_col_pos = 0
                step = 0
                while printing_current_element:
                    self.canvas[canvas_row_pos][canvas_col_pos] = element.pixel_array[element_row_pos][element_col_pos]
                    # Increment the canvas and element positions
                    if canvas_col_pos < canvas_col_stop:
                        if element_col_pos < element.width - 1:
                            canvas_col_pos += 1
                            element_col_pos += 1
                        else:
                            if element_row_pos < element.height -1:
                                element_col_pos = 0
                                element_row_pos += 1
                            else:
                                printing_current_element = False
                    elif canvas_row_pos < canvas_row_stop:
                        if element_row_pos < element.height -1:
                            canvas_col_pos = canvas_row_start
                            canvas_row_pos += 1
                            element_col_pos = 0
                            element_row_pos += 1
                        else:
                            printing_current_element = False
                    else:
                        printing_current_element = False




    def display(self):
        canvas_string = ''
        for row in range(self.height):
            for col in range(self.width):
                canvas_string += self.canvas[row][col]
            canvas_string += '\n' if row < self.height-1 else ''
        print(canvas_string, end='')

    def get_elements(self) -> list:
        if self.pages:
            return self.pages.get_elements()
        else:
            raise Exception('no page_collection exists for the screen')

    def step(self):
        self.update_screen_size()
        self.render_border()
        self.render_elements(1, self.width-2, 1, self.height-2, self.get_elements())
        self.clear()
        self.display()
