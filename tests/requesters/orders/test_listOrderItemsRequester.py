from unittest import TestCase, TestSuite, makeSuite, main

import requests

from mwstools.requesters.orders import ListOrderItemsRequester, ListOrderItemsResponse
from mwstools.parsers.errors import ErrorElement, InvalidParameterValue
from mwstools.mws_overrides import MWSResponse


def make_response(status_code, body):
    r = MWSResponse()
    r.status_code = status_code
    r._content = body
    return r


class TestListOrderItemsRequesterFailedBody(TestCase):
    """
    Test to make sure that the requester is raising on a status code 200 but the body is an ErrorResponse
    """

    body = """
    <ErrorResponse xmlns="https://mws.amazonservices.com/Orders/2013-09-01">
        <Error>
            <Type>Sender</Type>
            <Code>InvalidParameterValue</Code>
            <Message>Invalid AmazonOrderId: xxx-xxxxxxx-xxxxxxx</Message>
        </Error>
        <RequestId>request-id</RequestId>
    </ErrorResponse>
    """

    def setUp(self):
        self.requester = ListOrderItemsRequester(None, None, None)
        self.requester.api.list_order_items = lambda *args, **kwargs: make_response(200, self.body)

    def test_request(self):
        self.assertRaises(InvalidParameterValue, self.requester.request, None)


class TestListOrderItemsRequesterServerError(TestCase):
    body = ""

    def setUp(self):
        self.requester = ListOrderItemsRequester(None, None, None)
        self.requester.api.list_order_items = lambda *args, **kwargs: make_response(500, self.body)

    def raise_failed_request(self):
        self.requester.request(None)

    def test_request(self):
        self.assertRaises(requests.HTTPError, self.raise_failed_request)


class TestListOrderItemsRequesterClientError(TestCase):
    body = """
    <ErrorResponse xmlns="https://mws.amazonservices.com/Orders/2013-09-01">
        <Error>
            <Type>Sender</Type>
            <Code>InvalidParameterValue</Code>
            <Message>Invalid AmazonOrderId: xxx-xxxxxxx-xxxxxxx</Message>
        </Error>
        <RequestId>request-id</RequestId>
    </ErrorResponse>
    """

    def setUp(self):
        self.requester = ListOrderItemsRequester(None, None, None)
        self.requester.api.list_order_items = lambda *args, **kwargs: make_response(400, self.body)

    def raise_failed_request(self):
        self.requester.request(None)

    def test_request(self):
        self.assertRaises(InvalidParameterValue, self.raise_failed_request)


class TestListOrderItemsRequesterSuccess(TestCase):

    body = """
    <ListOrderItemsResponse xmlns="https://mws.amazonservices.com/Orders/2013-09-01">
        <Empty />
    </ListOrderItemsResponse>
    """

    def setUp(self):
        self.requester = ListOrderItemsRequester(None, None, None)
        self.requester.api.list_order_items = lambda *args, **kwargs: make_response(200, self.body)

    def test_request(self):
        self.assertIsInstance(self.requester.request(None), ListOrderItemsResponse)


__all__ = [
    TestListOrderItemsRequesterClientError,
    TestListOrderItemsRequesterFailedBody,
    TestListOrderItemsRequesterServerError,
    TestListOrderItemsRequesterSuccess
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')

