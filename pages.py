
from .custom_exceptions import NoElement, InvalidElement, ElementOverflow
from .elements import Element, ElementCollection, NoneElement


class Page:
    """
    Parent class for all `pages`. Holds an arrangement of HTML-like elements to be printed to the screen.
    """
    def __init__(self, name: str):
        self.name = name

        self.element_collection = ElementCollection()
        self.active_element = NoneElement()
        self.select_locked = False

    def add_to_top(self, element: Element):
        self.element_collection.add_element(element, 0)

    def add(self, element: Element):
        self.element_collection.add_element(element)

    def clear_elements(self):
        self.element_collection = []

    def select_next(self):
        if not self.select_locked:
            try:
                self.active_element = self.element_collection.select_next()
            except InvalidElement as e:
                # TODO: create a logger to hold exceptions
                pass

    def select_previous(self):
        if not self.select_locked:
            try:
                self.active_element = self.element_collection.select_previous()
            except InvalidElement as e:
                # TODO: create a logger to hold exceptions
                pass

    def act(self):
        pass


class PageCollection:
    """
    Holds a single instance of all our pages. This class can be passed to the display / controller module in order
    to give easy access to all of our page objects.
    """
    def __init__(self):

        self.page_list = []
        self.active_page = None
        self.menu_bar = None
        self.notifications = None

    def active_page_elements(self):
        pass

    def menubar_elements(self):
        pass

    def notification_elements(self):
        pass

    def select_next(self):
        pass

    def select_previous(self):
        pass

    def next_page(self):
        pass

    def act(self):
        pass

    def step(self):
        pass
