from unittest import TestCase, TestSuite, makeSuite, main

from mwstools.parsers.reports import RequestReportResponse, ReportRequestInfo


class RequestReportResponseTests(TestCase):
    body = """
    <RequestReportResponse xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
        <RequestReportResult>
            <ReportRequestInfo>
                <Empty />
            </ReportRequestInfo>
        </RequestReportResult>
        <ResponseMetadata>
            <RequestId>request-id</RequestId>
        </ResponseMetadata>
    </RequestReportResponse>
    """

    def setUp(self):
        self.parser = RequestReportResponse.load(self.body)

    def test__request_report_result(self):
        self.assertIsNotNone(self.parser._request_report_result)

    def test_request_report_result(self):
        self.assertIsInstance(self.parser.request_report_result, ReportRequestInfo)

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'request-id')


__all__ = [
    RequestReportResponseTests
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
