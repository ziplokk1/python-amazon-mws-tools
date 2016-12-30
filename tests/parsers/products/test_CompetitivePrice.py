from unittest import TestCase, TestSuite, makeSuite, main

from mwstools.parsers.products import CompetitivePrice


class TestCompetitivePriceNoCompetitivePrices(TestCase):

    body = """
    <Empty xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01" />
    """

    def setUp(self):
        self.parser = CompetitivePrice.load(self.body)

    def test_belongs_to_requester(self):
        self.assertIsNone(self.parser.belongs_to_requester)

    def test_condition(self):
        self.assertIsNone(self.parser.condition)

    def test_sub_condition(self):
        self.assertIsNone(self.parser.sub_condition)

    def test_competitive_price_id(self):
        self.assertIsNone(self.parser.competitive_price_id)

    def test_landed_price(self):
        self.assertIsNone(self.parser.landed_price)

    def test_listing_price(self):
        self.assertIsNone(self.parser.listing_price)

    def test_shipping(self):
        self.assertIsNone(self.parser.shipping)


class TestCompetitivePriceSuccess(TestCase):

    body = """
    <CompetitivePrice belongsToRequester="false" condition="New" subcondition="New" xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <CompetitivePriceId>1</CompetitivePriceId>
        <Price>
            <LandedPrice>
                <CurrencyCode>USD</CurrencyCode>
                <Amount>76.63</Amount>
            </LandedPrice>
            <ListingPrice>
                <CurrencyCode>USD</CurrencyCode>
                <Amount>76.63</Amount>
            </ListingPrice>
            <Shipping>
                <CurrencyCode>USD</CurrencyCode>
                <Amount>0.00</Amount>
            </Shipping>
        </Price>
    </CompetitivePrice>
    """

    def setUp(self):
        self.parser = CompetitivePrice.load(self.body)

    def test_belongs_to_requester(self):
        self.assertFalse(self.parser.belongs_to_requester)

    def test_condition(self):
        self.assertEqual(self.parser.condition, "New")

    def test_sub_condition(self):
        self.assertEqual(self.parser.sub_condition, "New")

    def test_competitive_price_id(self):
        self.assertEqual(self.parser.competitive_price_id, "1")

    def test_landed_price(self):
        self.assertEqual(self.parser.landed_price, "76.63")

    def test_listing_price(self):
        self.assertEqual(self.parser.listing_price, "76.63")

    def test_shipping(self):
        self.assertEqual(self.parser.shipping, "0.00")


__all__ = [
    TestCompetitivePriceNoCompetitivePrices,
    TestCompetitivePriceSuccess
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
