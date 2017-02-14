from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.reports import GetReportListResponse


class TestGetReportListResponse(TestCase):

    body = """
    <GetReportListResponse xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
        <GetReportListResult>
            <HasNext>true</HasNext>
            <NextToken>next-token</NextToken>
            <ReportInfo>
                <Empty />
            </ReportInfo>
            <ReportInfo>
                <Empty />
            </ReportInfo>
            <ReportInfo>
                <Empty />
            </ReportInfo>
            <ReportInfo>
                <Empty />
            </ReportInfo>
            <ReportInfo>
                <Empty />
            </ReportInfo>
            <ReportInfo>
                <Empty />
            </ReportInfo>
            <ReportInfo>
                <Empty />
            </ReportInfo>
            <ReportInfo>
                <Empty />
            </ReportInfo>
            <ReportInfo>
                <Empty />
            </ReportInfo>
            <ReportInfo>
                <Empty />
            </ReportInfo>
        </GetReportListResult>
        <ResponseMetadata>
            <RequestId>request-id</RequestId>
        </ResponseMetadata>
    </GetReportListResponse>
    """

    def setUp(self):
        self.parser = GetReportListResponse.load(self.body)

    def test_has_next(self):
        self.assertTrue(self.parser.has_next)

    def test_next_token(self):
        self.assertEqual(self.parser.next_token, 'next-token')

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'request-id')

    def test_report_info_list(self):
        self.assertEqual(len(self.parser.report_info_list()), 10)


__all__ = [
    TestGetReportListResponse
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')

