from .base import BaseElementWrapper, first_element, parse_date, parse_bool


class FeedSubmissionInfo(BaseElementWrapper):
    namespaces = {'a': 'http://mws.amazonaws.com/doc/2009-01-01/'}
    attrs = [
        'feed_processing_status',
        'feed_type',
        'feed_submission_id',
        'started_processing_date',
        'submitted_date',
        'completed_processing_date']

    @property
    @first_element
    def feed_processing_status(self):
        return self.xpath('./a:FeedProcessingStatus/text()')

    @property
    @first_element
    def feed_type(self):
        return self.xpath('./a:FeedType/text()')

    @property
    @first_element
    def feed_submission_id(self):
        return self.xpath('./a:FeedSubmissionId/text()')

    @property
    @parse_date
    @first_element
    def started_processing_date(self):
        return self.xpath('./a:StartedProcessingDate/text()')

    @property
    @parse_date
    @first_element
    def submitted_date(self):
        return self.xpath('./a:SubmittedDate/text()')

    @property
    @parse_date
    @first_element
    def completed_processing_date(self):
        return self.xpath('./a:CompletedProcessingDate/text()')

    def __repr__(self):
        return '<{} feed_submission_id={} feed_processing_status={}>'.format(
            self.__class__.__name__,
            self.feed_submission_id,
            self.feed_processing_status
        )


class SubmitFeedResponse(BaseElementWrapper):
    namespaces = {'a': 'http://mws.amazonaws.com/doc/2009-01-01/'}
    attrs = ['feed_submission_info',
             'request_id']

    @property
    @first_element
    def feed_submission_info(self):
        """

        :return:
        :rtype: FeedSubmissionInfo
        """
        return [FeedSubmissionInfo(x) for x in self.xpath('./a:SubmitFeedResult/a:FeedSubmissionInfo')]

    @property
    @first_element
    def request_id(self):
        return self.xpath('./a:ResponseMetadata/a:RequestId/text()')

    def __repr__(self):
        return '<{} feed_submission_info={} request_id={}>'.format(
            self.__class__.__name__,
            repr(self.feed_submission_info),
            self.request_id
        )


class GetFeedSubmissionListResponse(BaseElementWrapper):
    namespaces = {'a': 'http://mws.amazonaws.com/doc/2009-01-01/'}
    attrs = ['has_next',
             'next_token',
             'feed_submission_info',
             'request_id']

    @property
    @parse_bool
    @first_element
    def has_next(self):
        return self.xpath('./a:GetFeedSubmissionListResult/a:HasNext/text()')

    @property
    @first_element
    def next_token(self):
        return self.xpath('./a:GetFeedSubmissionListResult/a:NextToken/text()')

    @property
    def feed_submission_info(self):
        return [FeedSubmissionInfo(x) for x in self.xpath('./a:GetFeedSubmissionListResult/a:FeedSubmissionInfo')]

    @property
    @first_element
    def request_id(self):
        return self.xpath('./a:ResponseMetadata/a:RequestId/text()')

    def __repr__(self):
        return '<{} feed_submission_info={} request_id={}>'.format(
            self.__class__.__name__,
            [repr(x) for x in self.feed_submission_info],
            self.request_id
        )
