from unittest import TestCase, TestSuite, makeSuite, main
import datetime

from mwstools.parsers.reports import ReportRequestInfo


class TestReportRequestInfoSuccess(TestCase):

    body = """
    <ReportRequestInfo xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
      <ReportType>_ENUMERATION_TYPE_</ReportType>
      <ReportProcessingStatus>_DONE_</ReportProcessingStatus>
      <EndDate>2016-12-16T06:00:00+00:00</EndDate>
      <Scheduled>false</Scheduled>
      <ReportRequestId>report-request-id</ReportRequestId>
      <StartedProcessingDate>2016-12-16T22:02:07+00:00</StartedProcessingDate>
      <SubmittedDate>2016-12-16T22:02:02+00:00</SubmittedDate>
      <StartDate>2016-11-16T06:00:00+00:00</StartDate>
      <CompletedDate>2016-12-16T22:02:44+00:00</CompletedDate>
      <GeneratedReportId>generated-report-id</GeneratedReportId>
    </ReportRequestInfo>
    """

    def setUp(self):
        self.parser = ReportRequestInfo.load(self.body)

    def test_report_request_id(self):
        self.assertEqual(self.parser.report_request_id, 'report-request-id')

    def test_report_type(self):
        self.assertEqual(self.parser.report_type, '_ENUMERATION_TYPE_')

    def test_start_date(self):
        self.assertEqual(self.parser.start_date, datetime.datetime(2016, 11, 16, 1, 0, 0))

    def test_end_date(self):
        self.assertEqual(self.parser.end_date, datetime.datetime(2016, 12, 16, 1, 0, 0))

    def test_scheduled(self):
        self.assertFalse(self.parser.scheduled)

    def test_submitted_date(self):
        self.assertEqual(self.parser.submitted_date, datetime.datetime(2016, 12, 16, 17, 2, 2))

    def test_report_processing_status(self):
        self.assertEqual(self.parser.report_processing_status, '_DONE_')

    def test_completed_date(self):
        self.assertEqual(self.parser.completed_date, datetime.datetime(2016, 12, 16, 17, 2, 44))

    def test_started_processing_date(self):
        self.assertEqual(self.parser.started_processing_date, datetime.datetime(2016, 12, 16, 17, 2, 7))

    def test_generated_report_id(self):
        self.assertEqual(self.parser.generated_report_id, 'generated-report-id')


__all__ = [
    TestReportRequestInfoSuccess
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')

