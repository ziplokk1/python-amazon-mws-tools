from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.notifications import LowestPrice


class TestLowestPrice(TestCase):

    body = """
    <LowestPrice condition="new" fulfillmentChannel="Amazon">
        <LandedPrice>
            <Amount>12.15</Amount>
            <CurrencyCode>USD</CurrencyCode>
        </LandedPrice>
        <ListingPrice>
            <Amount>12.15</Amount>
            <CurrencyCode>USD</CurrencyCode>
        </ListingPrice>
        <Shipping>
            <Amount>0.00</Amount>
            <CurrencyCode>USD</CurrencyCode>
        </Shipping>
    </LowestPrice>
    """

    def setUp(self):
        self.parser = LowestPrice.load(self.body)

    def test_condition(self):
        self.assertEqual(self.parser.condition, 'new')

    def test_fulfillment_channel(self):
        self.assertEqual(self.parser.fulfillment_channel, 'Amazon')

    def test_landed_price(self):
        self.assertEqual(self.parser.landed_price, '12.15')

    def test_listing_price(self):
        self.assertEqual(self.parser.listing_price, '12.15')

    def test_shipping(self):
        self.assertEqual(self.parser.shipping, '0.00')

__all__ = [
    TestLowestPrice
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
