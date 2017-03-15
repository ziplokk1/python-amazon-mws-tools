from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.products.get_my_price_for_sku import Offer


class TestOffer(TestCase):
    body = """
    <Offer xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <BuyingPrice>
            <LandedPrice>
                <CurrencyCode>USD</CurrencyCode>
                <Amount>35.99</Amount>
            </LandedPrice>
            <ListingPrice>
                <CurrencyCode>USD</CurrencyCode>
                <Amount>35.99</Amount>
            </ListingPrice>
            <Shipping>
                <CurrencyCode>USD</CurrencyCode>
                <Amount>0.00</Amount>
            </Shipping>
        </BuyingPrice>
        <RegularPrice>
            <CurrencyCode>USD</CurrencyCode>
            <Amount>35.99</Amount>
        </RegularPrice>
        <FulfillmentChannel>AMAZON</FulfillmentChannel>
        <ItemCondition>New</ItemCondition>
        <ItemSubCondition>New</ItemSubCondition>
        <SellerId>seller-id</SellerId>
        <SellerSKU>seller-sku</SellerSKU>
    </Offer>
    """

    def setUp(self):
        self.parser = Offer.load(self.body)

    def test_landed_price(self):
        self.assertEqual(self.parser.landed_price, '35.99')

    def test_listing_price(self):
        self.assertEqual(self.parser.listing_price, '35.99')

    def test_shipping(self):
        self.assertEqual(self.parser.shipping, '0.00')

    def test_regular_price(self):
        self.assertEqual(self.parser.regular_price, '35.99')

    def test_fulfillment_channel(self):
        self.assertEqual(self.parser.fulfillment_channel, 'AMAZON')

    def test_item_condition(self):
        self.assertEqual(self.parser.item_condition, 'New')

    def test_item_sub_condition(self):
        self.assertEqual(self.parser.item_sub_condition, 'New')

    def test_seller_id(self):
        self.assertEqual(self.parser.seller_id, 'seller-id')

    def test_seller_sku(self):
        self.assertEqual(self.parser.seller_sku, 'seller-sku')


__all__ = [
    TestOffer,
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
