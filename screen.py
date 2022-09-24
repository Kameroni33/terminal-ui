import time

from .resources import constants
from .pages import PageCollection
from .display import Display
from .controller import Controller


class Screen:
    """
    Screen class
    """
    def __init__(self):
        self.page_collection = PageCollection()
        self.display = Display(self.page_collection)
        self.controller = Controller(self.page_collection, self.display)

    def play(self):
        while True:
            self.display.step()
            self.controller.step()
            self.page_collection.step()
            time.sleep(constants.REFRESH_RATE)
