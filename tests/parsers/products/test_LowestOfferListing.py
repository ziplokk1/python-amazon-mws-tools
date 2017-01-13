from unittest import TestCase
from mwstools.parsers.products import GetLowestOfferListingsForAsinResult, LowestOfferListingProduct


class TestLowestOfferListing(TestCase):

    body = """
    <GetLowestOfferListingsForASINResult ASIN="asin" status="Success" xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <AllOfferListingsConsidered>false</AllOfferListingsConsidered>
        <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                 xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
            <Empty />
        </Product>
    </GetLowestOfferListingsForASINResult>
    """

    def setUp(self):
        self.parser = GetLowestOfferListingsForAsinResult.load(self.body)

    def test_asin(self):
        self.assertEqual(self.parser.asin, 'asin')

    def test_status(self):
        self.assertEqual(self.parser.status, 'Success')

    def test_is_successful(self):
        self.assertTrue(self.parser.is_successful())

    def test_all_offer_listings_considered(self):
        self.assertFalse(self.parser.all_offer_listings_considered)

    def test_products(self):
        self.assertIsNotNone(self.parser.product())
        self.assertIsInstance(self.parser.product(), LowestOfferListingProduct)
