from unittest import TestCase, TestSuite, makeSuite, main

from mwstools.parsers.orders import ListOrdersResponse, ListOrdersResult


class TestListOrdersResponse(TestCase):

    body = """
    <ListOrdersResponse xmlns="https://mws.amazonservices.com/Orders/2013-09-01">
        <ListOrdersResult>
            <Orders>
                <Order>
                    <Empty />
                </Order>
            </Orders>
            <LastUpdatedBefore>2016-12-22T17:37:50Z</LastUpdatedBefore>
            <NextToken>next-token</NextToken>
        </ListOrdersResult>
        <ResponseMetadata>
            <RequestId>request-id</RequestId>
        </ResponseMetadata>
    </ListOrdersResponse>
    """

    def setUp(self):
        self.parser = ListOrdersResponse.load(self.body)

    def test__list_orders_result(self):
        self.assertIsNotNone(self.parser._list_orders_result)

    def test_list_orders_result(self):
        self.assertIsInstance(self.parser.list_orders_result, ListOrdersResult)

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'request-id')

# ToDo: Test from next token response

__all__ = [
    TestListOrdersResponse
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')

