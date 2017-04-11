import unittest
import datetime

from mwstools.parsers.base import first_element, parse_bool, parse_date


class WrapperFunctionTests(unittest.TestCase):
    def test_first_element_none(self):
        """
        Xpath will return none if the element is not found.

        :return:
        """

        def bogus():
            return None

        self.assertIsNone(first_element(bogus)())

    def test_first_element(self):
        def bogus():
            return [1, 2, 3]

        self.assertEqual(first_element(bogus)(), 1)

    def test_parse_bool_none(self):
        """
        Xpath will return none if the element is not found.
        :return:
        """

        def bogus():
            return None

        self.assertFalse(parse_bool(bogus)())

    def test_parse_bool_false(self):
        def bogus():
            return 'false'

        self.assertFalse(parse_bool(bogus)())

    def test_parse_bool_true(self):
        def bogus():
            return 'true'

        self.assertTrue(parse_bool(bogus)())

    def test_parse_date_none(self):
        """
        Xpath will return none if the element is not found.
        :return:
        """

        def bogus():
            return None

        self.assertIsNone(parse_date(bogus)())

    @unittest.expectedFailure
    def test_parse_invalid_date(self):
        def bogus():
            return 'this-date-is-invalid'

        self.assertIsNone(parse_date(bogus)())

    def test_parse_valid_date(self):
        def bogus():
            return '2001-01-01T06:00:00+00:00'

        self.assertEqual(parse_date(bogus)(), datetime.datetime(2001, 1, 1, 1, 0, 0))


__all__ = [
    WrapperFunctionTests
]


def suite():
    s = unittest.TestSuite()
    for a in __all__:
        s.addTest(unittest.makeSuite(a))
    return s


if __name__ == '__main__':
    unittest.main(defaultTest='suite')

