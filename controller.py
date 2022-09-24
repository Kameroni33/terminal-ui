import keyboard

from .resources import constants
from .pages import PageCollection
from .display import Display


class Controller:
    text_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

    def __init__(self, page_collection: PageCollection, display: Display):
        self._pages = page_collection
        self._display = display

        self.parse_input = False
        self.pressed = []
        self.pos = 1

        self.navigation_characters = [
            ('Esc', exit),
            ('f5', self._display.refresh),
            ('Down', self._pages.select_next),
            ('Right', self._pages.select_next),
            ('Up', self._pages.select_previous),
            ('Left', self._pages.select_previous),
            ('Enter', self._pages.act),
        ]

    def do_nothing(self):
        pass

    def poll_inputs(self):
        # Handle navigational input
        if not self.parse_input:
            for key in self.navigation_characters:
                if keyboard.is_pressed(key[0]):
                    if key[0] not in self.pressed:
                        for i in range(1, len(key)):
                            result = key[i]()
                            if result == 'parse_input':
                                self.parse_input = True
                        self.pressed.append(key[0])
                else:
                    self.pressed.remove(key[0]) if key[0] in self.pressed else None

        # Handle text input
        else:
            if keyboard.is_pressed('\b'):
                if '\b' not in self.pressed:
                    self._pages.active_page.active_element.linked_element.remove_char()
                    self.pressed.append('\b')
            else:
                self.pressed.remove('\b') if '\b' in self.pressed else None

            if keyboard.is_pressed('Enter'):
                if 'Enter' not in self.pressed:
                    self._pages.act()
                    self.parse_input = False
                    self.pressed.append('Enter')
            else:
                self.pressed.remove('Enter') if 'Enter' in self.pressed else None
            for letter in self.text_characters:
                if keyboard.is_pressed(letter):
                    if letter not in self.pressed:
                        self._pages.active_page.active_element.linked_element.add_char(letter)
                        self.pressed.append(letter)
                else:
                    self.pressed.remove(letter) if letter in self.pressed else None

    def step(self):
        self.poll_inputs()

