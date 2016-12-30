from unittest import TestCase, TestSuite, makeSuite, main

from mwstools.parsers.orders import OrderItem


class TestOrderItemSuccess(TestCase):

    body = """
    <OrderItem xmlns="https://mws.amazonservices.com/Orders/2013-09-01">
        <QuantityOrdered>1</QuantityOrdered>
        <Title>Title</Title>
        <PromotionDiscount>
            <CurrencyCode>USD</CurrencyCode>
            <Amount>0.00</Amount>
        </PromotionDiscount>
        <ASIN>asin</ASIN>
        <SellerSKU>sku</SellerSKU>
        <OrderItemId>xxxxxxxxxxxxxx</OrderItemId>
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
    """

    def setUp(self):
        self.parser = OrderItem.load(self.body, None)

    def test_quantity_ordered(self):
        self.assertEqual(self.parser.quantity_ordered, '1')

    def test_title(self):
        self.assertEqual(self.parser.title, 'Title')

    def test_promotion_discount(self):
        self.assertEqual(self.parser.promotion_discount, '0.00')

    def test_currency_code(self):
        self.assertEqual(self.parser.currency_code, 'USD')

    def test_asin(self):
        self.assertEqual(self.parser.asin, 'asin')

    def test_seller_sku(self):
        self.assertEqual(self.parser.seller_sku, 'sku')

    def test_order_item_id(self):
        self.assertEqual(self.parser.order_item_id, 'xxxxxxxxxxxxxx')

    def test_quantity_shipped(self):
        self.assertEqual(self.parser.quantity_shipped, '1')

    def test_item_price(self):
        self.assertEqual(self.parser.item_price, '13.11')

    def test_item_tax(self):
        self.assertEqual(self.parser.item_tax, '0.00')

__all__ = [
    TestOrderItemSuccess
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
