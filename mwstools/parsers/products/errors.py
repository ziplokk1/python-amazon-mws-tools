from ..errors import ErrorElement


class ProductError(ErrorElement):

    def __init__(self, element, identifier, status):
        super(ProductError, self).__init__(element)
        self.identifier = identifier
        self.status = status


class FeesError(ProductError):
    pass
