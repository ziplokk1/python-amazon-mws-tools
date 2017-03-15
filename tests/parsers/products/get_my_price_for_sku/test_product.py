from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.products.get_my_price_for_sku import Product


class TestProduct(TestCase):

    body = """
    <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
             xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
        <Identifiers>
            <MarketplaceASIN>
                <MarketplaceId>marketplace-id</MarketplaceId>
                <ASIN>asin</ASIN>
            </MarketplaceASIN>
            <SKUIdentifier>
                <MarketplaceId>marketplace-id</MarketplaceId>
                <SellerId>seller-id</SellerId>
                <SellerSKU>seller-sku</SellerSKU>
            </SKUIdentifier>
        </Identifiers>
        <Offers>
            <Offer>
                <Empty />
            </Offer>
        </Offers>
    </Product>
    """

    def setUp(self):
        self.parser = Product.load(self.body)

    def test_marketplace_id(self):
        self.assertEqual(self.parser.marketplace_id, 'marketplace-id')

    def test_asin(self):
        self.assertEqual(self.parser.asin, 'asin')

    def test_seller_id(self):
        self.assertEqual(self.parser.seller_id, 'seller-id')

    def test_seller_sku(self):
        self.assertEqual(self.parser.seller_sku, 'seller-sku')

    def test_offers(self):
        self.assertEqual(len(self.parser.offers), 1)


__all__ = [
    TestProduct,
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
