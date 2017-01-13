from unittest import TestCase
from mwstools.parsers.products import LowestOfferListing


class TestLowestOfferListing(TestCase):

    body = """
    <LowestOfferListing xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <Qualifiers>
            <ItemCondition>New</ItemCondition>
            <ItemSubcondition>New</ItemSubcondition>
            <FulfillmentChannel>Merchant</FulfillmentChannel>
            <ShipsDomestically>Unknown</ShipsDomestically>
            <ShippingTime>
                <Max>3-7 days</Max>
            </ShippingTime>
            <SellerPositiveFeedbackRating>95-97%</SellerPositiveFeedbackRating>
        </Qualifiers>
        <NumberOfOfferListingsConsidered>1</NumberOfOfferListingsConsidered>
        <SellerFeedbackCount>13669</SellerFeedbackCount>
        <Price>
            <LandedPrice>
                <CurrencyCode>USD</CurrencyCode>
                <Amount>14.08</Amount>
            </LandedPrice>
            <ListingPrice>
                <CurrencyCode>USD</CurrencyCode>
                <Amount>14.08</Amount>
            </ListingPrice>
            <Shipping>
                <CurrencyCode>USD</CurrencyCode>
                <Amount>0.00</Amount>
            </Shipping>
        </Price>
        <MultipleOffersAtLowestPrice>False</MultipleOffersAtLowestPrice>
    </LowestOfferListing>
    """

    def setUp(self):
        self.parser = LowestOfferListing.load(self.body)

    def test_item_condition(self):
        self.assertEqual(self.parser.item_condition, 'New')

    def test_item_subcondition(self):
        self.assertEqual(self.parser.item_subcondition, 'New')

    def test_fulfillment_channel(self):
        self.assertEqual(self.parser.fulfillment_channel, 'Merchant')

    def test_is_fba(self):
        self.assertFalse(self.parser.is_fba())

    def test_ships_domestically(self):
        self.assertEqual(self.parser.ships_domestically, 'Unknown')

    def test_shipping_time_max(self):
        self.assertEqual(self.parser.shipping_time_max, '3-7 days')

    def test_seller_positive_feedback_rating(self):
        self.assertEqual(self.parser.seller_positive_feedback_rating, '95-97%')

    def test_number_of_offer_listings_considered(self):
        self.assertEqual(self.parser.number_of_offer_listings_considered, '1')

    def test_seller_feedback_count(self):
        self.assertEqual(self.parser.seller_feedback_count, '13669')

    def test_currency_code(self):
        self.assertEqual(self.parser.currency_code, 'USD')

    def test_landed_price(self):
        self.assertEqual(self.parser.landed_price, '14.08')

    def test_listing_price(self):
        self.assertEqual(self.parser.listing_price, '14.08')

    def test_shipping(self):
        self.assertEqual(self.parser.shipping, '0.00')

    def test_multiple_offers_at_lowest_price(self):
        self.assertFalse(self.parser.multiple_offers_at_lowest_price)
