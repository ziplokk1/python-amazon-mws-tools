from ..parsers.errors import ErrorResponse
from warnings import warn


def raise_for_error(f):
    """
    Wrapper method to parse any error response and raise the ErrorResponse instance if an error is encountered.

    :param f:
    :return:
    """
    def inner(*args, **kwargs):
        warn('`raise_for_error` is deprecated and will not process any response content.')
        return f(*args, **kwargs)
        # e = ErrorResponse.load(content)
        # e.raise_for_error()
        # return content
    return inner


def raise_response_for_error(f):
    """
    Wrapper method to parse a response object and raise the ErrorResponse
    instance if an error is encountered in the response body.

    :param f:
    :return:
    """
    def inner(*args, **kwargs):
        warn('`raise_response_for_error` is deprecated and will not process any response content.')
        return f(*args, **kwargs)
    return inner
