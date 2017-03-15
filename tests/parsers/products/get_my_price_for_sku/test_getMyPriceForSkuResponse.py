from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.products.get_my_price_for_sku import GetMyPriceForSkuResponse

class TestGetMyPriceForSkuResponse(TestCase):

    body = """
    <GetMyPriceForSKUResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <GetMyPriceForSKUResult>
            <Empty />
        </GetMyPriceForSKUResult>
        <ResponseMetadata>
            <RequestId>request-id</RequestId>
        </ResponseMetadata>
    </GetMyPriceForSKUResponse>
    """

    def setUp(self):
        self.parser = GetMyPriceForSkuResponse.load(self.body)

    def test_get_my_price_for_sku_results(self):
        self.assertEqual(len(self.parser.get_my_price_for_sku_results), 1)

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'request-id')


__all__ = [
    TestGetMyPriceForSkuResponse,
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
