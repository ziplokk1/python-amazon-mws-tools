from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.notifications import Offer


class TestOffer(TestCase):

    body = """
    <Offer>
        <SellerId>seller-id</SellerId>
        <SubCondition>new</SubCondition>
        <SellerFeedbackRating>
            <SellerPositiveFeedbackRating>100</SellerPositiveFeedbackRating>
            <FeedbackCount>4806</FeedbackCount>
        </SellerFeedbackRating>
        <ShippingTime minimumHours="0" maximumHours="0" availabilityType="NOW"/>
        <ListingPrice>
            <Amount>12.15</Amount>
            <CurrencyCode>USD</CurrencyCode>
        </ListingPrice>
        <Shipping>
            <Amount>0.00</Amount>
            <CurrencyCode>USD</CurrencyCode>
        </Shipping>
        <IsFulfilledByAmazon>true</IsFulfilledByAmazon>
        <IsBuyBoxWinner>true</IsBuyBoxWinner>
        <IsFeaturedMerchant>true</IsFeaturedMerchant>
        <ShipsDomestically>true</ShipsDomestically>
    </Offer>
    """

    def setUp(self):
        self.parser = Offer.load(self.body)

    def test_seller_id(self):
        self.assertEqual(self.parser.seller_id, 'seller-id')

    def test_subcondition(self):
        self.assertEqual(self.parser.subcondition, 'new')

    def test_seller_positive_feedback_rating(self):
        self.assertEqual(self.parser.seller_positive_feedback_rating, '100')

    def test_feedback_count(self):
        self.assertEqual(self.parser.feedback_count, '4806')

    def test_shipping_minimum_hours(self):
        self.assertEqual(self.parser.shipping_minimum_hours, '0')

    def test_shipping_maximum_hours(self):
        self.assertEqual(self.parser.shipping_maximum_hours, '0')

    def test_shipping_availability_type(self):
        self.assertEqual(self.parser.shipping_availability_type, 'NOW')

    def test_listing_price(self):
        self.assertEqual(self.parser.listing_price, '12.15')

    def test_shipping(self):
        self.assertEqual(self.parser.shipping, '0.00')

    def test_calculated_landed_price(self):
        self.assertEqual(self.parser.calculated_landed_price(), 12.15)

    def test_is_fba(self):
        self.assertTrue(self.parser.is_fba)

    def test_is_buybox_winner(self):
        self.assertTrue(self.parser.is_buybox_winner)

    def test_is_featured_merchant(self):
        self.assertTrue(self.parser.is_featured_merchant)

    def test_ships_domestically(self):
        self.assertTrue(self.parser.ships_domestically)

__all__ = [
    TestOffer
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
