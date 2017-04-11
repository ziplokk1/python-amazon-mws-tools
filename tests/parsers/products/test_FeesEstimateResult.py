from unittest import TestCase
import datetime
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.products.get_my_fees_estimate import FeesEstimateResult
from mwstools.parsers.products.errors import FeesError


class TestFeesEstimateResult(TestCase):
    body = """
    <FeesEstimateResult xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <FeesEstimate>
            <TotalFeesEstimate>
                <CurrencyCode>USD</CurrencyCode>
                <Amount>18.72</Amount>
            </TotalFeesEstimate>
            <TimeOfFeesEstimation>2016-11-30T12:00:00.000Z</TimeOfFeesEstimation>
            <FeeDetailList>
                <FeeDetail>
                    <Empty />
                </FeeDetail>
                <FeeDetail>
                    <Empty />
                </FeeDetail>
                <FeeDetail>
                    <Empty />
                </FeeDetail>
                <FeeDetail>
                    <Empty />
                </FeeDetail>
            </FeeDetailList>
        </FeesEstimate>
        <FeesEstimateIdentifier>
            <MarketplaceId>marketplace-id</MarketplaceId>
            <IdType>ASIN</IdType>
            <SellerId>seller-id</SellerId>
            <IsAmazonFulfilled>true</IsAmazonFulfilled>
            <SellerInputIdentifier>seller-input-id</SellerInputIdentifier>
            <IdValue>asin</IdValue>
            <PriceToEstimateFees>
                <ListingPrice>
                    <CurrencyCode>USD</CurrencyCode>
                    <Amount>100.000000</Amount>
                </ListingPrice>
                <Shipping>
                    <CurrencyCode>USD</CurrencyCode>
                    <Amount>0.000000</Amount>
                </Shipping>
            </PriceToEstimateFees>
        </FeesEstimateIdentifier>
        <Status>Success</Status>
    </FeesEstimateResult>
    """

    def setUp(self):
        self.parser = FeesEstimateResult.load(self.body)

    def test_status(self):
        self.assertEqual(self.parser.status, 'Success')

    def test_is_success(self):
        self.assertTrue(self.parser.is_success())

    def test_marketplace_id(self):
        self.assertEqual(self.parser.marketplace_id, 'marketplace-id')

    def test_id_type(self):
        self.assertEqual(self.parser.id_type, 'ASIN')

    def test_seller_id(self):
        self.assertEqual(self.parser.seller_id, 'seller-id')

    def test_is_fba(self):
        self.assertTrue(self.parser.is_fba)

    def test_seller_input_identifier(self):
        self.assertEqual(self.parser.seller_input_identifier, 'seller-input-id')

    def test_id_value(self):
        self.assertEqual(self.parser.id_value, 'asin')

    def test_listing_price(self):
        self.assertEqual(self.parser.listing_price, '100.000000')

    def test_shipping(self):
        self.assertEqual(self.parser.shipping, '0.000000')

    def test_fee_detail_list(self):
        self.assertEqual(len(self.parser.fee_detail_list), 4)

    def test_total_fees_estimate(self):
        self.assertEqual(self.parser.total_fees_estimate, '18.72')

    def test_time_of_fees_estimation(self):
        self.assertEqual(self.parser.time_of_fees_estimation, datetime.datetime(2016, 11, 30, 7))

    def test_as_error(self):
        self.assertIsInstance(self.parser.as_error(), FeesError)
        self.assertFalse(self.parser.as_error())


class TestMissingCategoryFeesEstimateResult(TestCase):
    body = """
    <FeesEstimateResult xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <FeesEstimateIdentifier>
            <MarketplaceId>marketplace-id</MarketplaceId>
            <IdType>ASIN</IdType>
            <SellerId>seller-id</SellerId>
            <IsAmazonFulfilled>true</IsAmazonFulfilled>
            <SellerInputIdentifier>request-B00000JD5X</SellerInputIdentifier>
            <IdValue>B00000JD5X</IdValue>
            <PriceToEstimateFees>
                <ListingPrice>
                    <CurrencyCode>USD</CurrencyCode>
                    <Amount>100.000000</Amount>
                </ListingPrice>
                <Shipping>
                    <CurrencyCode>USD</CurrencyCode>
                    <Amount>0.000000</Amount>
                </Shipping>
            </PriceToEstimateFees>
        </FeesEstimateIdentifier>
        <Error>
            <Code>DataNotAvailable</Code>
            <Message>Non-buyable item. Missing category.</Message>
            <Type>Receiver</Type>
        </Error>
        <Status>ServerError</Status>
    </FeesEstimateResult>
    """

    def setUp(self):
        self.parser = FeesEstimateResult.load(self.body)

    def test_marketplace_id(self):
        self.assertEqual(self.parser.marketplace_id, 'marketplace-id')

    def test_id_type(self):
        self.assertEqual(self.parser.id_type, 'ASIN')

    def test_seller_id(self):
        self.assertEqual(self.parser.seller_id, 'seller-id')

    def test_is_fba(self):
        self.assertTrue(self.parser.is_fba)

    def test_seller_input_identifier(self):
        self.assertEqual(self.parser.seller_input_identifier, 'request-B00000JD5X')

    def test_id_value(self):
        self.assertEqual(self.parser.id_value, 'B00000JD5X')

    def test_listing_price(self):
        self.assertEqual(self.parser.listing_price, '100.000000')

    def test_shipping(self):
        self.assertEqual(self.parser.shipping, '0.000000')

    def test_fee_detail_list(self):
        self.assertEqual(len(self.parser.fee_detail_list), 0)

    def test_total_fees_estimate(self):
        self.assertIsNone(self.parser.total_fees_estimate)

    def test_time_of_fees_estimation(self):
        self.assertIsNone(self.parser.time_of_fees_estimation)

    def raise_error(self):
        raise self.parser.as_error()

    def test_as_error(self):
        self.assertIsInstance(self.parser.as_error(), FeesError)

    def test_as_error_raises(self):
        def _raise():
            raise self.parser.as_error()
        self.assertRaises(FeesError, _raise)

    def test_as_error_code(self):
        self.assertEqual(self.parser.as_error().code, 'DataNotAvailable')

    def test_as_error_type(self):
        self.assertEqual(self.parser.as_error().type, 'Receiver')

    def test_as_error_message(self):
        self.assertEqual(self.parser.as_error().message, 'Non-buyable item. Missing category.')


__all__ = [
    TestFeesEstimateResult,
    TestMissingCategoryFeesEstimateResult
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
