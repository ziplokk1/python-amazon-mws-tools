from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.notifications import OfferCount


class TestOfferCount(TestCase):

    body = """
    <OfferCount condition="new" fulfillmentChannel="Merchant">1</OfferCount>
    """

    def setUp(self):
        self.parser = OfferCount.load(self.body)

    def test_condition(self):
        self.assertEqual(self.parser.condition, 'new')

    def test_fulfillment_channel(self):
        self.assertEqual(self.parser.fulfillment_channel, 'Merchant')

    def test_count(self):
        self.assertEqual(self.parser.count, '1')

__all__ = [
    TestOfferCount
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
