import logging
from functools import partial

from lxml import etree

from ..utils import from_amazon_timestamp


def first_element_or_none(element_list):
    """
    Return the first element or None from an lxml selector result.
    :param element_list: lxml selector result
    :return:
    """
    if element_list:
        return element_list[0]
    return


def first_element(f):
    """
    function wrapper for _first_element_or_none.

    This is equivalent to using `return _first_element_or_none(xpath())`.
    :param f:
    :return:
    """
    def inner(*args, **kwargs):
        return first_element_or_none(f(*args, **kwargs))
    return inner


def parse_bool(f):
    """
    Parse boolean from string.

    :param f:
    :return:
    """
    def inner(*args, **kwargs):
        r = f(*args, **kwargs)
        if not r:
            return None
        return r.lower() == 'true'
    return inner


def parse_date(f):
    """
    Parse date from amazon timestamp.

    :param f:
    :return:
    """

    def inner(*args, **kwargs):
        ts = f(*args, **kwargs)
        if ts:
            return from_amazon_timestamp(ts)
        return
    return inner


class BaseElementWrapper(object):

    namespaces = {}
    # Used to create a dict from the instance attributes specified here.
    attrs = []
    orm_class = None

    def __init__(self, element):
        """

        :param element: Etree object of response body
        """
        # Assign placeholder element so that the partial on the elements xpath will not throw an error.
        if element is None:
            element = etree.fromstring('<Empty />')
        self.element = element

        self.xpath = partial(self.element.xpath, namespaces=self.namespaces)
        self.logger = logging.getLogger(self.__class__.__name__)

    def set_namespace(self, ns_dict):
        """
        Use this method to assign the namespace after the class has been instantiated.

        Otherwise the xpath method of this class will not update with the new namespace.

        :param ns_dict:
        :return:
        """
        self.namespaces = ns_dict
        self.xpath = partial(self.element.xpath, namespaces=ns_dict)

    def to_dict(self):
        d = {}
        for attr in self.attrs:
            result = self.__getattribute__(attr)
            # If attribute is callable, then call the method and store the result
            if callable(result):
                result = result()

            if isinstance(result, list):
                l = []
                for x in result:
                    if hasattr(x, 'to_dict'):
                        l.append(x.to_dict())
                    else:
                        l.append(x)
                d[attr] = l
            else:
                if hasattr(result, 'to_dict'):
                    d[attr] = result.to_dict()
                else:
                    d[attr] = result
        return d

    @property
    def __dict__(self):
        return self.to_dict()

    def __str__(self):
        return etree.tostring(self.element)

    @classmethod
    def string_to_element(cls, s):
        if not s:
            s = '<Empty />'
        return etree.fromstring(s)

    @classmethod
    def load(cls, xml_string):
        return cls(cls.string_to_element(xml_string))
