from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.products import GetMatchingProductForIdResponse


class TestGetMatchingProductForIdResponse(TestCase):

    body = """<?xml version="1.0"?>
    <GetMatchingProductForIdResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <GetMatchingProductForIdResult Id="082676082658" IdType="UPC" status="Success">
            <Empty />
        </GetMatchingProductForIdResult>
        <GetMatchingProductForIdResult Id="082676170065" IdType="UPC" status="Success">
            <Empty />
        </GetMatchingProductForIdResult>
        <GetMatchingProductForIdResult Id="082676247354" IdType="UPC" status="Success">
            <Empty />
        </GetMatchingProductForIdResult>
        <GetMatchingProductForIdResult Id="652695068850" IdType="UPC" status="Success">
            <Empty />
        </GetMatchingProductForIdResult>
        <GetMatchingProductForIdResult Id="847357005117" IdType="UPC" status="Success">
            <Empty />
        </GetMatchingProductForIdResult>
        <ResponseMetadata>
            <RequestId>request-id</RequestId>
        </ResponseMetadata>
    </GetMatchingProductForIdResponse>
    """

    def setUp(self):
        self.parser = GetMatchingProductForIdResponse.load(self.body)

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'request-id')

    def test_results(self):
        self.assertEqual(len(self.parser.results()), 5)


__all__ = [
    TestGetMatchingProductForIdResponse
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')

