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


def raise_response_for_error(f):
    """
    Wrapper method to parse a response object and raise the ErrorResponse
    instance if an error is encountered in the response body.
    :param f:
    :return:
    """
    def inner(*args, **kwargs):
        response = f(*args, **kwargs)
        response.raise_for_status()
        content = response.content
        e = ErrorResponse.load(content)
        e.raise_for_error()
        return response
    return inner
