from ..errors import ErrorElement, MwsResponseError


class ProductErrorElement(ErrorElement):

    def __init__(self, element, identifier, status):
        super(ProductErrorElement, self).__init__(element)
        self.identifier = identifier
        self.status = status


class ProductError(MwsResponseError):

    def __init__(self, type, code, message, identifier, status):
        self.identifier = identifier
        self.status = status
        super(ProductError, self).__init__(type, code, message)


class FeesError(ProductError):

    def __nonzero__(self):
        return bool(self.message)
