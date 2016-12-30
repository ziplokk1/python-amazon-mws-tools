from unittest import TestSuite, main
from test_ReportRequester import suite as suite_report_requester


def suite():
    s = TestSuite()
    s.addTest(suite_report_requester())
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
