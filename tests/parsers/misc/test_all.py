from unittest import TestSuite, main

from test_GetServiceStatusResponse import suite as suite_test_get_service_status_response


def suite():
    s = TestSuite()
    s.addTest((suite_test_get_service_status_response()))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')

