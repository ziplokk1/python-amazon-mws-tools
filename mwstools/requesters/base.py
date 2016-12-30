from ..parsers.errors import ErrorResponse


def raise_for_error(f):
    """
    Wrapper method to parse any error response and raise the ErrorResponse instance if an error is encountered.

    :param f:
    :return:
    """
    def inner(*args, **kwargs):
        content = f(*args, **kwargs)
        e = ErrorResponse.load(content)
        e.raise_for_error()
        return content
    return inner
