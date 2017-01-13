from unittest import TestCase
from mwstools.parsers.products import LowestOfferListingProduct


class TestLowestOfferListingProduct(TestCase):

    body = """
    <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                 xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
        <Identifiers>
            <MarketplaceASIN>
                <MarketplaceId>marketplace-id</MarketplaceId>
                <ASIN>asin</ASIN>
            </MarketplaceASIN>
        </Identifiers>
        <LowestOfferListings>
            <LowestOfferListing>
                <Empty />
            </LowestOfferListing>
        </LowestOfferListings>
    </Product>
    """

    def setUp(self):
        self.parser = LowestOfferListingProduct.load(self.body)

    def test_asin(self):
        self.assertEqual(self.parser.asin, 'asin')

    def test_marketplace_id(self):
        self.assertEqual(self.parser.marketplace_id, 'marketplace-id')

    def test_lowest_offer_listings(self):
        self.assertEqual(len(self.parser.lowest_offer_listings()), 1)
