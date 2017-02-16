from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.feeds import SubmitFeedResponse, FeedSubmissionInfo


class TestSubmitFeedResponse(TestCase):
    body = """
    <SubmitFeedResponse xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
    <SubmitFeedResult>
        <FeedSubmissionInfo>
            <Empty />
        </FeedSubmissionInfo>
    </SubmitFeedResult>
    <ResponseMetadata>
        <RequestId>request-id</RequestId>
    </ResponseMetadata>
    </SubmitFeedResponse>
    """

    def setUp(self):
        self.parser = SubmitFeedResponse.load(self.body)

    def test_feed_submission_info(self):
        self.assertIsInstance(self.parser.feed_submission_info, FeedSubmissionInfo)

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'request-id')


__all__ = [
    TestSubmitFeedResponse
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
