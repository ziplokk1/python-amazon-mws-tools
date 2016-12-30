from unittest import TestCase, TestSuite, main, makeSuite

from mwstools.parsers.products import OfferListingCount


class TestOfferListingCountSuccess(TestCase):

    body = """<OfferListingCount condition="New" xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">2</OfferListingCount>"""

    def setUp(self):
        self.parser = OfferListingCount.load(self.body)

    def test_count(self):
        self.assertEqual(self.parser.count, '2')

    def test_condition(self):
        self.assertEqual(self.parser.condition, 'New')


class TestOfferListingDoesNotExist(TestCase):

    body = """<Empty xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01" />"""

    def setUp(self):
        self.parser = OfferListingCount.load(self.body)

    def test_count(self):
        self.assertIsNone(self.parser.count)

    def test_condition(self):
        self.assertIsNone(self.parser.condition)


__all__ = [
    TestOfferListingCountSuccess,
    TestOfferListingDoesNotExist
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')

