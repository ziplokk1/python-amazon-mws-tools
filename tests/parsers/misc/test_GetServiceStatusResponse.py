from unittest import TestCase

import datetime
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.get_service_status import GetServiceStatusResponse


class TestGetServiceStatusResponse(TestCase):

    body = """
    <GetServiceStatusResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
      <GetServiceStatusResult>
        <Status>GREEN</Status>
        <Timestamp>2017-02-21T06:00:00.000Z</Timestamp>
      </GetServiceStatusResult>
      <ResponseMetadata>
        <RequestId>request-id</RequestId>
      </ResponseMetadata>
    </GetServiceStatusResponse>
    """

    def setUp(self):
        self.parser = GetServiceStatusResponse.load(self.body)

    def test_status(self):
        self.assertEqual(self.parser.status, 'GREEN')

    def test_timestamp(self):
        self.assertEqual(self.parser.timestamp, datetime.datetime(2017, 2, 21, 1))

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'request-id')


__all__ = [
    TestGetServiceStatusResponse
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
