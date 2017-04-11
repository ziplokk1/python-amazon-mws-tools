from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite
from datetime import datetime

from mwstools.parsers.feeds import FeedSubmissionInfo


class TestFeedSubmissionInfoNoCompletedStarted(TestCase):
    body = """
    <FeedSubmissionInfo xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
        <FeedProcessingStatus>_DONE_</FeedProcessingStatus>
        <FeedType>_POST_FLAT_FILE_INVLOADER_DATA_</FeedType>
        <FeedSubmissionId>feed-submission-id</FeedSubmissionId>
        <SubmittedDate>2017-02-15T06:00:00+00:00</SubmittedDate>
    </FeedSubmissionInfo>
    """

    def setUp(self):
        self.parser = FeedSubmissionInfo.load(self.body)

    def test_feed_processing_status(self):
        self.assertEqual(self.parser.feed_processing_status, '_DONE_')

    def test_feed_type(self):
        self.assertEqual(self.parser.feed_type, '_POST_FLAT_FILE_INVLOADER_DATA_')

    def test_feed_submission_id(self):
        self.assertEqual(self.parser.feed_submission_id, 'feed-submission-id')

    def test_started_processing_date(self):
        self.assertIsNone(self.parser.started_processing_date)

    def test_submitted_date(self):
        self.assertEqual(self.parser.submitted_date, datetime(2017, 02, 15, 1))

    def test_completed_processing_date(self):
        self.assertIsNone(self.parser.completed_processing_date)


class TestFeedSubmissionInfoCompletedStarted(TestCase):
    body = """
    <FeedSubmissionInfo xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
        <FeedProcessingStatus>_DONE_</FeedProcessingStatus>
        <FeedType>_POST_FLAT_FILE_INVLOADER_DATA_</FeedType>
        <FeedSubmissionId>feed-submission-id</FeedSubmissionId>
        <StartedProcessingDate>2017-02-15T06:00:00+00:00</StartedProcessingDate>
        <SubmittedDate>2017-02-15T06:00:00+00:00</SubmittedDate>
        <CompletedProcessingDate>2017-02-15T06:00:00+00:00</CompletedProcessingDate>
    </FeedSubmissionInfo>
    """

    def setUp(self):
        self.parser = FeedSubmissionInfo.load(self.body)

    def test_feed_processing_status(self):
        self.assertEqual(self.parser.feed_processing_status, '_DONE_')

    def test_feed_type(self):
        self.assertEqual(self.parser.feed_type, '_POST_FLAT_FILE_INVLOADER_DATA_')

    def test_feed_submission_id(self):
        self.assertEqual(self.parser.feed_submission_id, 'feed-submission-id')

    def test_started_processing_date(self):
        self.assertEqual(self.parser.submitted_date, datetime(2017, 2, 15, 1))

    def test_submitted_date(self):
        self.assertEqual(self.parser.submitted_date, datetime(2017, 2, 15, 1))

    def test_completed_processing_date(self):
        self.assertEqual(self.parser.submitted_date, datetime(2017, 2, 15, 1))


__all__ = [
    TestFeedSubmissionInfoNoCompletedStarted,
    TestFeedSubmissionInfoCompletedStarted
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
