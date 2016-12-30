from unittest import TestCase, TestSuite, makeSuite, main

from mwstools.parsers.reports import GetReportRequestListResponse


class TestGetReportRequestListResponseSuccess(TestCase):

    body = """
    <GetReportRequestListResponse xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
        <GetReportRequestListResult>
            <NextToken>bogus-token</NextToken>
            <HasNext>true</HasNext>
            <ReportRequestInfo>
                <Empty />
            </ReportRequestInfo>
        </GetReportRequestListResult>
        <ResponseMetadata>
            <RequestId>c156a0bb-1e31-4c63-8226-7f996d75dfc8</RequestId>
        </ResponseMetadata>
    </GetReportRequestListResponse>
    """

    def setUp(self):
        self.parser = GetReportRequestListResponse.load(self.body)

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'c156a0bb-1e31-4c63-8226-7f996d75dfc8')

    def test_has_next(self):
        self.assertTrue(self.parser.has_next)

    def test_next_token(self):
        self.assertEqual(self.parser.next_token, 'bogus-token')

    def test_report_request_info_list(self):
        self.assertEqual(len(self.parser.report_request_info_list()), 1)


class TestGetReportRequestListResponseSuccessNoNextToken(TestCase):

    body = """
    <GetReportRequestListResponse xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
        <GetReportRequestListResult>
            <ReportRequestInfo>
                <Emtpy />
            </ReportRequestInfo>
        </GetReportRequestListResult>
        <ResponseMetadata>
            <RequestId>c156a0bb-1e31-4c63-8226-7f996d75dfc8</RequestId>
        </ResponseMetadata>
    </GetReportRequestListResponse>
    """

    def setUp(self):
        self.parser = GetReportRequestListResponse.load(self.body)

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'c156a0bb-1e31-4c63-8226-7f996d75dfc8')

    def test_has_next(self):
        self.assertFalse(self.parser.has_next)

    def test_next_token(self):
        self.assertIsNone(self.parser.next_token)

    def test_report_request_info_list(self):
        self.assertEqual(len(self.parser.report_request_info_list()), 1)


__all__ = [
    TestGetReportRequestListResponseSuccess,
    TestGetReportRequestListResponseSuccessNoNextToken
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')

