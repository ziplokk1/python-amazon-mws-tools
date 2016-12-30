from unittest import TestCase, TestSuite, makeSuite, main

from mwstools.parsers.products import SalesRank


class TestSalesRankSuccess(TestCase):

    body = """
    <SalesRank xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <ProductCategoryId>jewelry_display_on_website</ProductCategoryId>
        <Rank>809814</Rank>
    </SalesRank>
    """

    def setUp(self):
        self.parser = SalesRank.load(self.body)

    def test_product_category_id(self):
        self.assertEqual(self.parser.product_category_id, 'jewelry_display_on_website')

    def test_rank(self):
        self.assertEqual(self.parser.rank, '809814')


class TestSalesRankDoesNotExist(TestCase):
    body = """
    <Empty xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01" />
    """

    def setUp(self):
        self.parser = SalesRank.load(self.body)

    def test_product_category_id(self):
        self.assertIsNone(self.parser.product_category_id)

    def test_rank(self):
        self.assertIsNone(self.parser.rank)


__all__ = [
    TestSalesRankDoesNotExist,
    TestSalesRankSuccess
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')

