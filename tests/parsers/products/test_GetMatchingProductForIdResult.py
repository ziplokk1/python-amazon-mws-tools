from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.products import GetMatchingProductForIdResult


class TestGetMatchingProductForIdResult(TestCase):

    body = """
    <GetMatchingProductForIdResult Id="082676082658" IdType="UPC" status="Success">
        <Products xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                  xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
            <Product>
                <Empty />
            </Product>
        </Products>
    </GetMatchingProductForIdResult>
    """

    def setUp(self):
        self.parser = GetMatchingProductForIdResult.load(self.body)

    def test_id_(self):
        self.assertEqual(self.parser.id_, '082676082658')

    def test_id_type(self):
        self.assertEqual(self.parser.id_type, 'UPC')

    def test_status(self):
        self.assertEqual(self.parser.status, 'Success')

    def test_is_success(self):
        self.assertTrue(self.parser.is_success())

    def test_products(self):
        self.assertEqual(len(self.parser.products()), 1)


__all__ = [
    TestGetMatchingProductForIdResult
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')

