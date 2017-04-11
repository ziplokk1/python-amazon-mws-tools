from unittest import TestCase
import datetime
from unittest import TestSuite
from unittest import expectedFailure
from unittest import makeSuite
from unittest import main

from mwstools.parsers.orders import Order


class TestOrderSuccess(TestCase):

    body = """
    <Order xmlns="https://mws.amazonservices.com/Orders/2013-09-01">
        <LatestShipDate>2016-12-21T17:14:23Z</LatestShipDate>
        <OrderType>StandardOrder</OrderType>
        <PurchaseDate>2016-12-21T00:55:17Z</PurchaseDate>
        <BuyerEmail>email@marketplace.amazon.com</BuyerEmail>
        <AmazonOrderId>xxx-xxxxxxx-xxxxxxx</AmazonOrderId>
        <LastUpdateDate>2016-12-21T17:39:55Z</LastUpdateDate>
        <ShipServiceLevel>SecondDay</ShipServiceLevel>
        <NumberOfItemsShipped>1</NumberOfItemsShipped>
        <OrderStatus>Shipped</OrderStatus>
        <SalesChannel>Amazon.com</SalesChannel>
        <NumberOfItemsUnshipped>0</NumberOfItemsUnshipped>
        <BuyerName>Buyer Name</BuyerName>
        <OrderTotal>
            <CurrencyCode>USD</CurrencyCode>
            <Amount>6.24</Amount>
        </OrderTotal>
        <EarliestShipDate>2016-12-21T17:14:23Z</EarliestShipDate>
        <MarketplaceId>marketplace-id</MarketplaceId>
        <FulfillmentChannel>AFN</FulfillmentChannel>
        <PaymentMethod>Other</PaymentMethod>
        <ShippingAddress>
            <StateOrRegion>TEXAS</StateOrRegion>
            <City>CITY</City>
            <CountryCode>US</CountryCode>
            <PostalCode>zip-code</PostalCode>
            <Name>Shipping Address Name</Name>
            <AddressLine1>Address Line 1</AddressLine1>
        </ShippingAddress>
        <ShipmentServiceLevelCategory>SecondDay</ShipmentServiceLevelCategory>
        <SellerOrderId>xxx-xxxxxxx-xxxxxxx</SellerOrderId>
    </Order>
    """

    def setUp(self):
        self.parser = Order.load(self.body)

    def test_latest_ship_date(self):
        self.assertEqual(self.parser.latest_ship_date, datetime.datetime(2016, 12, 21, 12, 14, 23))

    def test_order_type(self):
        self.assertEqual(self.parser.order_type, 'StandardOrder')

    def test_purchase_date(self):
        self.assertEqual(self.parser.purchase_date, datetime.datetime(2016, 12, 20, 19, 55, 17))

    def test_buyer_email(self):
        self.assertEqual(self.parser.buyer_email, 'email@marketplace.amazon.com')

    def test_amazon_order_id(self):
        self.assertEqual(self.parser.amazon_order_id, 'xxx-xxxxxxx-xxxxxxx')

    def test_last_update_date(self):
        self.assertEqual(self.parser.last_update_date, datetime.datetime(2016, 12, 21, 12, 39, 55))

    def test_number_of_items_shipped(self):
        self.assertEqual(self.parser.number_of_items_shipped, '1')

    def test_ship_service_level(self):
        self.assertEqual(self.parser.ship_service_level, 'SecondDay')

    def test_order_status(self):
        self.assertEqual(self.parser.order_status, 'Shipped')

    def test_sales_channel(self):
        self.assertEqual(self.parser.sales_channel, 'Amazon.com')

    # ToDo: find order with this attribute
    @expectedFailure
    def test_is_business_order(self):
        self.fail()

    def test_number_of_items_unshipped(self):
        self.assertEqual(self.parser.number_of_items_unshipped, '0')

    def test_buyer_name(self):
        self.assertEqual(self.parser.buyer_name, 'Buyer Name')

    def test_currency_code(self):
        self.assertEqual(self.parser.currency_code, 'USD')

    def test_order_total(self):
        self.assertEqual(self.parser.order_total, '6.24')

    #ToDo: find order with this attribute
    @expectedFailure
    def test_is_premium_order(self):
        self.fail()

    def test_earliest_ship_date(self):
        self.assertEqual(self.parser.earliest_ship_date, datetime.datetime(2016, 12, 21, 12, 14, 23))

    def test_marketplace_id(self):
        self.assertEqual(self.parser.marketplace_id, 'marketplace-id')

    def test_fulfillment_channel(self):
        self.assertEqual(self.parser.fulfillment_channel, 'AFN')

    def test_payment_method(self):
        self.assertEqual(self.parser.payment_method, 'Other')

    # ToDo: find order with this attribute
    @expectedFailure
    def test_is_prime(self):
        self.fail()

    def test_shipment_service_level_category(self):
        self.assertEqual(self.parser.shipment_service_level_category, 'SecondDay')

    def test_seller_order_id(self):
        self.assertEqual(self.parser.seller_order_id, 'xxx-xxxxxxx-xxxxxxx')

    def test_state_or_region(self):
        self.assertEqual(self.parser.state_or_region, 'TEXAS')

    def test_ship_state_abbreviation(self):
        self.assertEqual(self.parser.ship_state_abbreviation, 'TX')

    def test_city(self):
        self.assertEqual(self.parser.city, 'CITY')

    # ToDo: find order with this attribute
    @expectedFailure
    def test_phone(self):
        self.fail()

    def test_country_code(self):
        self.assertEqual(self.parser.country_code, 'US')

    def test_postal_code(self):
        self.assertEqual(self.parser.postal_code, 'zip-code')

    def test_name(self):
        self.assertEqual(self.parser.name, 'Shipping Address Name')

    def test_address_line_1(self):
        self.assertEqual(self.parser.address_line_1, 'Address Line 1')

    def test_address_line_2(self):
        self.assertIsNone(self.parser.address_line_2)


__all__ = [
    TestOrderSuccess
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
