import os
import cursor

from .resources import constants, graphics
from .pages import PageCollection


class Display:

    def __init__(self, page_collection: PageCollection):
        self._pages = page_collection

        self.width = None
        self.height = None
        self.canvas = None
        self._refresh = False

        self.scroll_vertical = 0
        self.scroll_horizontal = 0

        os.system('cls')
        cursor.hide()

    def clear(self):
        if self._refresh:
            os.system('cls')
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

    def render_elements(self, canvas_row: int, canvas_col: int, elements: list, scroll=False):
        pass

    def display(self):
        screen_string = ''
        for row in range(self.height):
            for col in range(self.width):
                screen_string += self.canvas[row][col]
            screen_string += '\n' if row < self.height-1 else ''
        print(screen_string, end='')

    def step(self):
        self.update_screen_size()
        self.render_border()
        self.clear()
        self.display()
