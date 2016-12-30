from unittest import TestCase, TestSuite, makeSuite, main

from mwstools.parsers.orders import ListOrderItemsResponse


class TestListOrderItemsResponseInvalidOrderId(TestCase):
    """
    The use case of this test is just to make sure that none of the data is returned since
    the error response will be parsed out by another method and raised appropriately.
    """

    body = """
    <ErrorResponse xmlns="https://mws.amazonservices.com/Orders/2013-09-01">
        <Error>
            <Type>Sender</Type>
            <Code>InvalidParameterValue</Code>
            <Message>Invalid AmazonOrderId: asdf</Message>
        </Error>
        <RequestId>request-id</RequestId>
    </ErrorResponse>
    """

    def setUp(self):
        self.parser = ListOrderItemsResponse.load(self.body)

    def test_has_next(self):
        self.assertFalse(self.parser.has_next())

    def test_next_token(self):
        self.assertIsNone(self.parser.next_token)

    def test_amazon_order_id(self):
        self.assertIsNone(self.parser.amazon_order_id)

    def test_order_items(self):
        self.assertEqual(len(self.parser.order_items()), 0)

    def test_request_id(self):
        self.assertIsNone(self.parser.request_id)


class TestListOrderItemsResponseSuccess(TestCase):

    body = """
    <ListOrderItemsResponse xmlns="https://mws.amazonservices.com/Orders/2013-09-01">
        <ListOrderItemsResult>
            <OrderItems>
                <OrderItem>
                    <QuantityOrdered>1</QuantityOrdered>
                    <Title>title</Title>
                    <PromotionDiscount>
                        <CurrencyCode>USD</CurrencyCode>
                        <Amount>0.00</Amount>
                    </PromotionDiscount>
                    <ASIN>asin</ASIN>
                    <SellerSKU>sku</SellerSKU>
                    <OrderItemId>order-item-id</OrderItemId>
                    <QuantityShipped>1</QuantityShipped>
                    <ItemPrice>
                        <CurrencyCode>USD</CurrencyCode>
                        <Amount>13.11</Amount>
                    </ItemPrice>
                    <ItemTax>
                        <CurrencyCode>USD</CurrencyCode>
                        <Amount>0.00</Amount>
                    </ItemTax>
                </OrderItem>
            </OrderItems>
            <AmazonOrderId>xxx-xxxxxxx-xxxxxxx</AmazonOrderId>
        </ListOrderItemsResult>
        <ResponseMetadata>
            <RequestId>request-id</RequestId>
        </ResponseMetadata>
    </ListOrderItemsResponse>
    """

    def setUp(self):
        self.parser = ListOrderItemsResponse.load(self.body)

    def test_has_next(self):
        self.assertFalse(self.parser.has_next())

    def test_next_token(self):
        self.assertIsNone(self.parser.next_token)

    def test_amazon_order_id(self):
        self.assertEqual(self.parser.amazon_order_id, 'xxx-xxxxxxx-xxxxxxx')

    def test_order_items(self):
        self.assertEqual(len(self.parser.order_items()), 1)

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'request-id')


__all__ = [
    TestListOrderItemsResponseInvalidOrderId,
    TestListOrderItemsResponseSuccess
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')

