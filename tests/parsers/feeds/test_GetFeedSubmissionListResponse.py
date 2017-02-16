from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.feeds import GetFeedSubmissionListResponse, FeedSubmissionInfo


class TestGetFeedSubmissionListResponseNoNextToken(TestCase):
    body = """
          <GetFeedSubmissionListResponse xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
          <GetFeedSubmissionListResult>
            <HasNext>false</HasNext>
            <FeedSubmissionInfo>
              <empty />
            </FeedSubmissionInfo>
          </GetFeedSubmissionListResult>
          <ResponseMetadata>
            <RequestId>request-id</RequestId>
          </ResponseMetadata>
          </GetFeedSubmissionListResponse>
        """

    def setUp(self):
        self.parser = GetFeedSubmissionListResponse.load(self.body)

    def test_has_next(self):
        self.assertFalse(self.parser.has_next)

    def test_next_token(self):
        self.assertIsNone(self.parser.next_token)

    def test_feed_submission_info_length(self):
        self.assertEqual(len(self.parser.feed_submission_info), 1)

    def test_feed_submission_info_type(self):
        self.assertIsInstance(self.parser.feed_submission_info[0], FeedSubmissionInfo)

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'request-id')


class TestGetFeedSubmissionListResponseNextToken(TestCase):
    body = """
          <GetFeedSubmissionListResponse xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
          <GetFeedSubmissionListResult>
            <HasNext>true</HasNext>
            <NextToken>next-token</NextToken>
            <FeedSubmissionInfo>
              <empty />
            </FeedSubmissionInfo>
          </GetFeedSubmissionListResult>
          <ResponseMetadata>
            <RequestId>request-id</RequestId>
          </ResponseMetadata>
          </GetFeedSubmissionListResponse>
        """

    def setUp(self):
        self.parser = GetFeedSubmissionListResponse.load(self.body)

    def test_has_next(self):
        self.assertTrue(self.parser.has_next)

    def test_next_token(self):
        self.assertEqual(self.parser.next_token, 'next-token')

    def test_feed_submission_info_length(self):
        self.assertEqual(len(self.parser.feed_submission_info), 1)

    def test_feed_submission_info_type(self):
        self.assertIsInstance(self.parser.feed_submission_info[0], FeedSubmissionInfo)

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'request-id')


__all__ = [
    TestGetFeedSubmissionListResponseNoNextToken,
    TestGetFeedSubmissionListResponseNextToken
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
