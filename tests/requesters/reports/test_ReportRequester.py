from unittest import TestCase, TestSuite, makeSuite, main
from requests import HTTPError

from mws.mws import DictWrapper

from mwstools.parsers.errors import ErrorElement, InvalidParameterValue
from mwstools.requesters.reports import ReportRequester
from mwstools.mws_overrides import MWSResponse


successful_body = """

"""

failed_body = """
<ErrorResponse xmlns="https://mws.amazonservices.com/Orders/2011-01-01">
    <Error>
        <Type>Sender</Type>
        <Code>InvalidParameterValue</Code>
        <Message>CreatedAfter or LastUpdatedAfter must be specified</Message>
    </Error>
    <RequestId>bc28f262-5da9-4e75-a511-1995d309ce6c</RequestId>
</ErrorResponse>
"""

no_body = """"""


def make_response(status_code, body):
    r = MWSResponse()
    r.status_code = status_code
    r._content = body
    return r


class TestReportRequesterErrorResponse(TestCase):
    """
    Test ErrorResponse with 200 status code
    """

    def setUp(self):
        self.requester = ReportRequester(None, None, None, None)
        self.requester.api.request = lambda *args, **kwargs: make_response(200, failed_body)

    def raise_error_element_request(self):
        self.requester.request()

    def raise_error_element_get_report_status(self):
        self.requester.get_report_status(None)

    def test_request(self):
        """
        Make sure that the test fails when an error response comes back.
        :return:
        """
        self.assertRaises(InvalidParameterValue, self.raise_error_element_request)

    def test_error_get_report_status(self):
        """
        Make sure that the test fails when an error response comes back.
        :return:
        """
        self.assertRaises(InvalidParameterValue, self.raise_error_element_get_report_status)


class TestReportRequesterServerError(TestCase):
    """
    Test no content returned with 500 status code
    """

    def setUp(self):
        self.requester = ReportRequester(None, None, None, None)
        self.requester.api.request = lambda *args, **kwargs: make_response(500, no_body)

    def raise_http_error_request(self):
        self.requester.request()

    def raise_http_error_get_report_status(self):
        self.requester.get_report_status(None)

    def test_request(self):
        """
        Make sure that the test fails when an error response comes back.
        :return:
        """
        self.assertRaises(HTTPError, self.raise_http_error_request)

    def test_error_get_report_status(self):
        """
        Make sure that the test fails when an error response comes back.
        :return:
        """
        self.assertRaises(HTTPError, self.raise_http_error_get_report_status)


__all__ = [
    TestReportRequesterErrorResponse,
    TestReportRequesterServerError
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
