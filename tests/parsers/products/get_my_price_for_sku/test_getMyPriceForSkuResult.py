from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.products.get_my_price_for_sku import GetMyPriceForSkuResult, Product


class TestGetMyPriceForSkuResult(TestCase):

    body = """
    <GetMyPriceForSKUResult SellerSKU="seller-sku" status="Success" xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                 xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
            <Empty />
        </Product>
    </GetMyPriceForSKUResult>
    """

    def setUp(self):
        self.parser = GetMyPriceForSkuResult.load(self.body)

    def test_seller_sku(self):
        self.assertEqual(self.parser.seller_sku, 'seller-sku')

    def test_status(self):
        self.assertEqual(self.parser.status, 'Success')

    def test_is_success(self):
        self.assertTrue(self.parser.is_success())

    def test__product(self):
        self.assertIsNotNone(self.parser._product)

    def test_product(self):
        self.assertIsInstance(self.parser.product, Product)


__all__ = [
    TestGetMyPriceForSkuResult,
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
