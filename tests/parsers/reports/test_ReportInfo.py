from unittest import TestCase
import datetime
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.reports import ReportInfo


class TestReportInfoNotAcknowledged(TestCase):

    body = """
    <ReportInfo xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
        <ReportType>_GET_MERCHANT_LISTINGS_DATA_</ReportType>
        <Acknowledged>false</Acknowledged>
        <ReportId>report-id</ReportId>
        <ReportRequestId>report-request-id</ReportRequestId>
        <AvailableDate>2017-02-14T06:00:00+00:00</AvailableDate>
    </ReportInfo>
    """

    def setUp(self):
        self.parser = ReportInfo.load(self.body)

    def test_report_type(self):
        self.assertEqual(self.parser.report_type, '_GET_MERCHANT_LISTINGS_DATA_')

    def test_acknowledged(self):
        self.assertFalse(self.parser.acknowledged)

    def test_acknowledged_date(self):
        self.assertIsNone(self.parser.acknowledged_date)

    def test_report_id(self):
        self.assertEqual(self.parser.report_id, 'report-id')

    def test_report_request_id(self):
        self.assertEqual(self.parser.report_request_id, 'report-request-id')

    def test_available_date(self):
        self.assertEqual(self.parser.available_date, datetime.datetime(2017, 2, 14, 1))


class TestReportInfoAcknowledged(TestCase):

    body = """
    <ReportInfo xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
        <ReportType>_GET_MERCHANT_LISTINGS_DATA_</ReportType>
        <Acknowledged>true</Acknowledged>
        <AcknowledgedDate>2017-02-14T06:00:00+00:00</AcknowledgedDate>
        <ReportId>report-id</ReportId>
        <ReportRequestId>report-request-id</ReportRequestId>
        <AvailableDate>2017-02-14T06:00:00+00:00</AvailableDate>
    </ReportInfo>
    """

    def setUp(self):
        self.parser = ReportInfo.load(self.body)

    def test_report_type(self):
        self.assertEqual(self.parser.report_type, '_GET_MERCHANT_LISTINGS_DATA_')

    def test_acknowledged(self):
        self.assertTrue(self.parser.acknowledged)

    def test_acknowledged_date(self):
        self.assertEqual(self.parser.acknowledged_date, datetime.datetime(2017, 2, 14, 1))

    def test_report_id(self):
        self.assertEqual(self.parser.report_id, 'report-id')

    def test_report_request_id(self):
        self.assertEqual(self.parser.report_request_id, 'report-request-id')

    def test_available_date(self):
        self.assertEqual(self.parser.available_date, datetime.datetime(2017, 2, 14, 1))


__all__ = [
    TestReportInfoAcknowledged,
    TestReportInfoNotAcknowledged
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
