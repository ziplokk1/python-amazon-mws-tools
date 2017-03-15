from unittest import TestCase, TestSuite, makeSuite, main

from mwstools.parsers.products import Product, ProductErrorElement
from mwstools.parsers.products.errors import ProductError


class TestClientError(TestCase):

    body = """
    <GetCompetitivePricingForASINResult ASIN="asin" status="ClientError" xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <Error>
            <Type>Sender</Type>
            <Code>InvalidParameterValue</Code>
            <Message>ASIN asin is not valid for marketplace ATVPDKIKX0DER</Message>
        </Error>
    </GetCompetitivePricingForASINResult>
    """

    def setUp(self):
        self.parser = Product.load(self.body)

    def test_asin(self):
        self.assertEqual(self.parser.asin, 'asin')

    def test_status(self):
        self.assertEqual(self.parser.status, 'ClientError')

    def test_marketplace_id(self):
        self.assertIsNone(self.parser.marketplace_id)

    def test_error(self):
        self.assertIsNotNone(self.parser.error)

    def test_competitive_prices(self):
        self.assertEqual(len(self.parser.competitive_prices()), 0)

    def test_number_of_offer_listings(self):
        self.assertEqual(len(self.parser.number_of_offer_listings()), 0)

    def test_sales_rankings(self):
        self.assertEqual(len(self.parser.sales_rankings()), 0)

    def test_website_ranking(self):
        self.assertIsNone(self.parser.website_ranking())

    def test_is_success(self):
        self.assertFalse(self.parser.is_success())

    def test_new_landed_price(self):
        self.assertIsNone(self.parser.new_landed_price())

    def test_raise(self):
        self.assertRaises(ProductError, self.parser.raise_for_error)


class TestNoCompetitivePrices(TestCase):

    body = """
    <GetCompetitivePricingForASINResult ASIN="asin" status="Success" xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                 xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
            <Identifiers>
                <MarketplaceASIN>
                    <MarketplaceId>markplace-id</MarketplaceId>
                    <ASIN>asin</ASIN>
                </MarketplaceASIN>
            </Identifiers>
            <CompetitivePricing>
                <CompetitivePrices/>
                <NumberOfOfferListings>
                    <OfferListingCount condition="New">35</OfferListingCount>
                    <OfferListingCount condition="Any">35</OfferListingCount>
                </NumberOfOfferListings>
            </CompetitivePricing>
            <SalesRankings>
                <SalesRank>
                    <ProductCategoryId>health_and_beauty_display_on_website</ProductCategoryId>
                    <Rank>3455</Rank>
                </SalesRank>
                <SalesRank>
                    <ProductCategoryId>3760991</ProductCategoryId>
                    <Rank>17</Rank>
                </SalesRank>
            </SalesRankings>
        </Product>
    </GetCompetitivePricingForASINResult>
    """

    def setUp(self):
        self.parser = Product.load(self.body)

    def test_asin(self):
        self.assertEqual(self.parser.asin, 'asin')

    def test_status(self):
        self.assertEqual(self.parser.status, 'Success')

    def test_marketplace_id(self):
        self.assertEqual(self.parser.marketplace_id, 'markplace-id')

    def test_error(self):
        self.assertFalse(self.parser.error)

    def test_competitive_prices(self):
        self.assertEqual(len(self.parser.competitive_prices()), 0)

    def test_number_of_offer_listings(self):
        self.assertEqual(len(self.parser.number_of_offer_listings()), 2)

    def test_sales_rankings(self):
        self.assertEqual(len(self.parser.sales_rankings()), 2)

    def test_website_ranking(self):
        self.assertEqual(self.parser.website_ranking(), '3455')

    def test_is_success(self):
        self.assertTrue(self.parser.is_success())

    def test_new_landed_price(self):
        self.assertIsNone(self.parser.new_landed_price())

    def test_raise(self):
        try:
            self.parser.raise_for_error()
        except ProductErrorElement:
            self.fail('raise_for_error() raised ProductError unexpectedly.')


class TestMultipleSalesRankings(TestCase):

    body = """
    <GetCompetitivePricingForASINResult ASIN="asin" status="Success" xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                 xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
            <Identifiers>
                <MarketplaceASIN>
                    <MarketplaceId>marketplace-id</MarketplaceId>
                    <ASIN>asin</ASIN>
                </MarketplaceASIN>
            </Identifiers>
            <CompetitivePricing>
                <CompetitivePrices>
                    <CompetitivePrice belongsToRequester="false" condition="New" subcondition="New">
                        <CompetitivePriceId>1</CompetitivePriceId>
                        <Price>
                            <LandedPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>32.95</Amount>
                            </LandedPrice>
                            <ListingPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>32.95</Amount>
                            </ListingPrice>
                            <Shipping>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>0.00</Amount>
                            </Shipping>
                        </Price>
                    </CompetitivePrice>
                </CompetitivePrices>
                <NumberOfOfferListings>
                    <OfferListingCount condition="New">1</OfferListingCount>
                    <OfferListingCount condition="Any">1</OfferListingCount>
                </NumberOfOfferListings>
            </CompetitivePricing>
            <SalesRankings>
                <SalesRank>
                    <ProductCategoryId>home_garden_display_on_website</ProductCategoryId>
                    <Rank>3619885</Rank>
                </SalesRank>
                <SalesRank>
                    <ProductCategoryId>3734401</ProductCategoryId>
                    <Rank>2413</Rank>
                </SalesRank>
                <SalesRank>
                    <ProductCategoryId>13679441</ProductCategoryId>
                    <Rank>3334</Rank>
                </SalesRank>
            </SalesRankings>
        </Product>
    </GetCompetitivePricingForASINResult>
    """

    def setUp(self):
        self.parser = Product.load(self.body)

    def test_asin(self):
        self.assertEqual(self.parser.asin, 'asin')

    def test_status(self):
        self.assertEqual(self.parser.status, 'Success')

    def test_marketplace_id(self):
        self.assertEqual(self.parser.marketplace_id, 'marketplace-id')

    def test_error(self):
        self.assertFalse(self.parser.error)

    def test_competitive_prices(self):
        self.assertEqual(len(self.parser.competitive_prices()), 1)

    def test_number_of_offer_listings(self):
        self.assertEqual(len(self.parser.number_of_offer_listings()), 2)

    def test_sales_rankings(self):
        self.assertEqual(len(self.parser.sales_rankings()), 3)

    def test_website_ranking(self):
        self.assertEqual(self.parser.website_ranking(), '3619885')

    def test_is_success(self):
        self.assertTrue(self.parser.is_success())

    def test_new_landed_price(self):
        self.assertEqual(self.parser.new_landed_price(), '32.95')

    def test_raise(self):
        try:
            self.parser.raise_for_error()
        except ProductErrorElement:
            self.fail('raise_for_error() raised ProductError unexpectedly.')


class TestProductNoRanking(TestCase):

    body = """
    <GetCompetitivePricingForASINResult ASIN="asin" status="Success" xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                 xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
            <Identifiers>
                <MarketplaceASIN>
                    <MarketplaceId>marketplace-id</MarketplaceId>
                    <ASIN>asin</ASIN>
                </MarketplaceASIN>
            </Identifiers>
            <CompetitivePricing>
                <CompetitivePrices>
                    <CompetitivePrice belongsToRequester="false" condition="New" subcondition="New">
                        <CompetitivePriceId>1</CompetitivePriceId>
                        <Price>
                            <LandedPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>179.10</Amount>
                            </LandedPrice>
                            <ListingPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>179.10</Amount>
                            </ListingPrice>
                            <Shipping>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>0.00</Amount>
                            </Shipping>
                        </Price>
                    </CompetitivePrice>
                </CompetitivePrices>
                <NumberOfOfferListings>
                    <OfferListingCount condition="New">2</OfferListingCount>
                    <OfferListingCount condition="Any">2</OfferListingCount>
                </NumberOfOfferListings>
            </CompetitivePricing>
            <SalesRankings/>
        </Product>
    </GetCompetitivePricingForASINResult>
    """

    def setUp(self):
        self.parser = Product.load(self.body)

    def test_asin(self):
        self.assertEqual(self.parser.asin, 'asin')

    def test_status(self):
        self.assertEqual(self.parser.status, 'Success')

    def test_marketplace_id(self):
        self.assertEqual(self.parser.marketplace_id, 'marketplace-id')

    def test_error(self):
        self.assertFalse(self.parser.error)

    def test_competitive_prices(self):
        self.assertEqual(len(self.parser.competitive_prices()), 1)

    def test_number_of_offer_listings(self):
        self.assertEqual(len(self.parser.number_of_offer_listings()), 2)

    def test_sales_rankings(self):
        self.assertEqual(len(self.parser.sales_rankings()), 0)

    def test_website_ranking(self):
        self.assertIsNone(self.parser.website_ranking())

    def test_is_success(self):
        self.assertTrue(self.parser.is_success())

    def test_new_landed_price(self):
        self.assertEqual(self.parser.new_landed_price(), '179.10')

    def test_raise(self):
        try:
            self.parser.raise_for_error()
        except ProductErrorElement:
            self.fail('raise_for_error() raised ProductError unexpectedly.')


class TestProductSuccess(TestCase):
    """
    Testing product parser with valid competitive prices, rankings, offer listings, and successful request.
    """

    body = """
    <GetCompetitivePricingForASINResult ASIN="asin" status="Success" xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                 xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
            <Identifiers>
                <MarketplaceASIN>
                    <MarketplaceId>marketplace-id</MarketplaceId>
                    <ASIN>asin</ASIN>
                </MarketplaceASIN>
            </Identifiers>
            <CompetitivePricing>
                <CompetitivePrices>
                    <CompetitivePrice belongsToRequester="false" condition="New" subcondition="New">
                        <CompetitivePriceId>1</CompetitivePriceId>
                        <Price>
                            <LandedPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>179.10</Amount>
                            </LandedPrice>
                            <ListingPrice>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>179.10</Amount>
                            </ListingPrice>
                            <Shipping>
                                <CurrencyCode>USD</CurrencyCode>
                                <Amount>0.00</Amount>
                            </Shipping>
                        </Price>
                    </CompetitivePrice>
                </CompetitivePrices>
                <NumberOfOfferListings>
                    <OfferListingCount condition="New">2</OfferListingCount>
                    <OfferListingCount condition="Any">2</OfferListingCount>
                </NumberOfOfferListings>
            </CompetitivePricing>
            <SalesRankings>
                <SalesRank>
                    <ProductCategoryId>jewelry_display_on_website</ProductCategoryId>
                    <Rank>974086</Rank>
                </SalesRank>
            </SalesRankings>
        </Product>
    </GetCompetitivePricingForASINResult>
    """

    def setUp(self):
        self.parser = Product.load(self.body)

    def test_asin(self):
        self.assertEqual(self.parser.asin, 'asin')

    def test_status(self):
        self.assertEqual(self.parser.status, 'Success')

    def test_marketplace_id(self):
        self.assertEqual(self.parser.marketplace_id, 'marketplace-id')

    def test_error(self):
        self.assertFalse(self.parser.error)

    def test_competitive_prices(self):
        self.assertEqual(len(self.parser.competitive_prices()), 1)

    def test_number_of_offer_listings(self):
        self.assertEqual(len(self.parser.number_of_offer_listings()), 2)

    def test_sales_rankings(self):
        self.assertEqual(len(self.parser.sales_rankings()), 1)

    def test_website_ranking(self):
        self.assertEqual(self.parser.website_ranking(), '974086')

    def test_is_success(self):
        self.assertTrue(self.parser.is_success())

    def test_new_landed_price(self):
        self.assertEqual(self.parser.new_landed_price(), '179.10')

    def test_raise(self):
        try:
            self.parser.raise_for_error()
        except ProductErrorElement:
            self.fail('raise_for_error() raised ProductError unexpectedly.')


__all__ = [
    TestProductSuccess,
    TestProductNoRanking,
    TestMultipleSalesRankings,
    TestNoCompetitivePrices,
    TestClientError
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
