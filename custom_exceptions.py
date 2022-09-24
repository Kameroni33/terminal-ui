
class ElementOverflow(Exception):
    def __init__(self, message):
        super().__init__(message)


class NoElement(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidElement(Exception):
    def __init__(self, message):
        super().__init__(message)
