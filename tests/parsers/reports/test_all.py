from unittest import TestSuite, main
from test_GetReportRequestListResponse import suite as suite_get_report_request_list_response
from test_RequestReportResponse import suite as suite_request_report_response
from test_ReportRequestInfo import suite as suite_report_request_info


def suite():
    s = TestSuite()
    s.addTest(suite_get_report_request_list_response())
    s.addTest(suite_request_report_response())
    s.addTest(suite_report_request_info())
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
