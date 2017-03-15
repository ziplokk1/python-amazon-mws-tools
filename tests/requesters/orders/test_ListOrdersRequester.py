from unittest import TestCase, TestSuite, makeSuite, main

import requests

from mwstools.parsers.errors import ErrorElement, InvalidParameterValue
from mwstools.parsers.orders import ListOrdersResponse
from mwstools.requesters.orders import ListOrdersRequester
from mwstools.mws_overrides import MWSResponse


def make_response(status_code, body):
    r = MWSResponse()
    r.status_code = status_code
    r._content = body
    return r


class TestListOrdersRequesterFailedBody(TestCase):
    """
    Test to make sure that the requester is raising on a status code 200 but the body is an ErrorResponse
    """

    body = """
    <ErrorResponse xmlns="https://mws.amazonservices.com/Orders/2013-09-01">
        <Error>
            <Type>Sender</Type>
            <Code>InvalidParameterValue</Code>
            <Message>CreatedAfter or LastUpdatedAfter must be specified</Message>
        </Error>
        <RequestId>request-id</RequestId>
    </ErrorResponse>
    """

    def setUp(self):
        self.requester = ListOrdersRequester(None, None, None)
        self.requester.api.list_orders = lambda *args, **kwargs: make_response(200, self.body)

    def raise_failed_request(self):
        self.requester.request()

    def test_request(self):
        self.assertRaises(InvalidParameterValue, self.raise_failed_request)


class TestListOrdersRequesterServerError(TestCase):
    body = ""

    def setUp(self):
        self.requester = ListOrdersRequester(None, None, None)
        self.requester.api.list_orders = lambda *args, **kwargs: make_response(500, self.body)

    def raise_failed_request(self):
        self.requester.request()

    def test_request(self):
        self.assertRaises(requests.HTTPError, self.raise_failed_request)


class TestListOrdersRequesterClientError(TestCase):
    """
    Despite the 400 status code, there is still a body and should be raised with ErrorElement.
    """

    body = """
    <ErrorResponse xmlns="https://mws.amazonservices.com/Orders/2013-09-01">
        <Error>
            <Type>Sender</Type>
            <Code>InvalidParameterValue</Code>
            <Message>CreatedAfter or LastUpdatedAfter must be specified</Message>
        </Error>
        <RequestId>request-id</RequestId>
    </ErrorResponse>
    """

    def setUp(self):
        self.requester = ListOrdersRequester(None, None, None)
        self.requester.api.list_orders = lambda *args, **kwargs: make_response(400, self.body)

    def raise_failed_request(self):
        self.requester.request()

    def test_request(self):
        self.assertRaises(InvalidParameterValue, self.raise_failed_request)


class TestListOrdersRequesterSuccess(TestCase):

    body = """
    <ListOrdersResponse xmlns="https://mws.amazonservices.com/Orders/2013-09-01">
        <Emtpy />
    </ListOrdersResponse>
    """

    def setUp(self):
        self.requester = ListOrdersRequester(None, None, None)
        self.requester.api.list_orders = lambda *args, **kwargs: make_response(200, self.body)

    def test_request(self):
        self.assertIsInstance(self.requester.request(), ListOrdersResponse)


__all__ = [
    TestListOrdersRequesterClientError,
    TestListOrdersRequesterFailedBody,
    TestListOrdersRequesterServerError,
    TestListOrdersRequesterSuccess
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
