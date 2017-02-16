from unittest import TestSuite, main
from test_FeedSubmissionInfo import suite as suite_test_feed_submission_info
from test_SubmitFeedResponse import suite as suite_test_submit_feed_response


def suite():
    s = TestSuite()
    s.addTest((suite_test_feed_submission_info()))
    s.addTest((suite_test_submit_feed_response()))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
