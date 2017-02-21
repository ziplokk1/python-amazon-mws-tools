import unittest

from parsers import products_suite, orders_suite, errors_suite, reports_suite, notifications_suite, feeds_suite, misc_suite as parsers_misc_suite
from requesters import reports_suite as requesters_reports_suite, orders_suite as requesters_orders_suite
from test_misc import suite as misc_suite


def suite():
    s = unittest.TestSuite()
    s.addTest(orders_suite())
    s.addTest(products_suite())
    s.addTest(reports_suite())
    s.addTest(errors_suite())
    s.addTest(notifications_suite())
    s.addTest(misc_suite())
    s.addTest(requesters_reports_suite())
    s.addTest(requesters_orders_suite())
    s.addTest(feeds_suite())
    s.addTest(parsers_misc_suite())
    return s

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
