import re

from lxml import etree

from .base import BaseElementWrapper, first_element


def _strip_namespace(s):
    """
    Remove all namespaces from the xml document.

    Required to make a parser for any error responses because the namespace will be different depending on the operation
    which received the error.
    :param s:
    :return:
    """
    doc = re.sub(r'\sxmlns=\".*?\"', '', s)
    return doc


def strip_namespace(element):
    """
    Remove all namespaces from the root element.

    :param element:
    :return:
    """
    if element is not None:
        xml_string = etree.tostring(element)
        xml_string = _strip_namespace(xml_string)
        element = etree.fromstring(xml_string)
    return element


class MwsResponseError(Exception):

    def __init__(self, type, code, message):
        self.type = type
        self.code = code
        self.message = message
        super(MwsResponseError, self).__init__(self, message)

    def __str__(self):
        return self.message


class InputStreamDisconnected(MwsResponseError):
    pass


class InvalidParameterValue(MwsResponseError):
    pass


class AccessDenied(MwsResponseError):
    pass


class InvalidAccessKey(MwsResponseError):
    pass


class SignatureDoesNotMatch(MwsResponseError):
    pass


class InvalidAddress(MwsResponseError):
    pass


class InternalError(MwsResponseError):
    pass


class QuotaExceeded(MwsResponseError):
    pass


class RequestThrottled(MwsResponseError):
    pass


_errors = {
    'InputStreamDisconnected': InputStreamDisconnected,
    'InvalidParameterValue': InvalidParameterValue,
    'AccessDenied': AccessDenied,
    'InvalidAccessKey': InvalidAccessKey,
    'SignatureDoesNotMatch': SignatureDoesNotMatch,
    'InvalidAddress': InvalidAddress,
    'InternalError': InternalError,
    'QuotaExceeded': QuotaExceeded,
    'RequestThrottled': RequestThrottled
}


def get_proper_error(error):
    E = _errors.get(error.code)
    if not E:
        return MwsResponseError(error.type, error.code, error.message)
    return E(error.type, error.code, error.message)


class ErrorElement(BaseElementWrapper):

    """
    Root element of <Error />
    """

    attrs = [
        'type',
        'code',
        'message'
    ]

    def __init__(self, element):
        # Remove namespace from element since depending on the API Operation, the namespace is different
        # yet the structure remains the same.
        element = strip_namespace(element)
        super(ErrorElement, self).__init__(element)
        self.xpath = self.element.xpath

    @property
    @first_element
    def type(self):
        return self.xpath('./Type/text()')

    @property
    @first_element
    def code(self):
        return self.xpath('./Code/text()')

    @property
    @first_element
    def message(self):
        return self.xpath('./Message/text()')

    def __nonzero__(self):
        return bool(self.xpath('/Error'))

    def __repr__(self):
        return '<{} type={} code={} message={}>'.format(
            self.__class__.__name__,
            self.type,
            self.code,
            self.message
        )


class ErrorResponse(BaseElementWrapper):

    attrs = [
        'request_id',
        'error'
    ]

    def __init__(self, element):
        element = strip_namespace(element)
        super(ErrorResponse, self).__init__(element)
        self.xpath = self.element.xpath

    @property
    @first_element
    def request_id(self):
        return self.xpath('./RequestId/text()')

    @property
    @first_element
    def _error(self):
        return self.xpath('./Error')

    @property
    def error(self):
        return ErrorElement(self._error)

    def raise_for_error(self):
        if self.error:
            raise get_proper_error(self.error)

    def __repr__(self):
        return "<{} request_id={} code={} message={}>".format(
            self.__class__.__name__,
            self.request_id,
            self.error.code,
            self.error.message
        )

