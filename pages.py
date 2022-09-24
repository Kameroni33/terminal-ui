
from .elements import Element, ElementCollection, NoneElement


class Page:
    """
    Parent class for all `pages`. Holds an arrangement elements to be printed to the screen.
    """
    def __init__(self, name: str):
        self.name = name

        self.element_collection = ElementCollection()
        self.active_element = None
        self.select_locked = False

    def add_to_top(self, element: Element):
        self.element_collection.add_element(element, 0)

    def add(self, element: Element):
        self.element_collection.add_element(element)

    def clear_elements(self):
        self.element_collection = []

    def get_elements(self) -> list:
        return self.element_collection.get_elements()

    def select_next(self):
        if not self.select_locked:
            try:
                self.active_element = self.element_collection.select_next()
            except Exception as e:
                # TODO: create a logger to hold exceptions
                pass

    def select_previous(self):
        if not self.select_locked:
            try:
                self.active_element = self.element_collection.select_previous()
            except Exception as e:
                # TODO: create a logger to hold exceptions
                pass

    def act(self):
        pass


class PageCollection:
    """
    Holds a single instance of all our pages. This class can be passed to the display / controller module in order
    to give easy access to all of our page objects.
    """
    def __init__(self, menu_bar: bool = False, notifications: bool = False):

        self.page_list = []
        self.active_page = None
        self.menu_bar = None
        self.notifications = None


        if menu_bar:
            self.menu_bar = None
        if notifications:
            self.notifications = None

    def add_page(self, page: Page):
        self.page_list.append(page)
        if len(self.page_list) == 1:
            self.active_page = page


    def delete_page(self, page_name: str):
        pass

    def get_elements(self) -> list:
        if self.active_page:
            return self.active_page.get_elements()
        else:
            raise Exception('there is no active page...')

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
