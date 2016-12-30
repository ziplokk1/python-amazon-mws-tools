from .base import BaseElementWrapper, first_element, parse_date, parse_bool


class GetReportRequestListResponse(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonaws.com/doc/2009-01-01/'}
    attrs = ['request_id', 'has_next', 'next_token', 'report_request_info_list']

    @property
    @first_element
    def request_id(self):
        return self.xpath('//a:RequestId/text()')

    @property
    @parse_bool
    @first_element
    def has_next(self):
        return self.xpath('//a:HasNext/text()')

    @property
    @first_element
    def next_token(self):
        return self.xpath('//a:NextToken/text()')

    def report_request_info_list(self):
        return [ReportRequestInfo(x) for x in self.xpath('//a:ReportRequestInfo')]


class RequestReportResponse(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonaws.com/doc/2009-01-01/'}
    attrs = ['request_report_result', 'request_id']

    @property
    def request_report_result(self):
        return ReportRequestInfo(self._request_report_result)

    @property
    @first_element
    def _request_report_result(self):
        return self.xpath('./a:RequestReportResult/a:ReportRequestInfo')

    @property
    @first_element
    def request_id(self):
        return self.xpath('//a:RequestId/text()')


class ReportRequestInfo(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonaws.com/doc/2009-01-01/'}
    attrs = [
        'report_request_id',
        'report_type',
        'start_date',
        'end_date',
        'scheduled',
        'submitted_date',
        'report_processing_status',
        'generated_report_id',
        'completed_date',
        'started_processing_date'
    ]

    @property
    @first_element
    def report_request_id(self):
        return self.xpath('./a:ReportRequestId/text()')

    @property
    @first_element
    def report_type(self):
        return self.xpath('./a:ReportType/text()')

    @property
    @parse_date
    @first_element
    def start_date(self):
        return self.xpath('./a:StartDate/text()')

    @property
    @parse_date
    @first_element
    def end_date(self):
        return self.xpath('./a:EndDate/text()')

    @property
    @parse_bool
    @first_element
    def scheduled(self):
        return self.xpath('./a:Scheduled/text()')

    @property
    @parse_date
    @first_element
    def submitted_date(self):
        return self.xpath('./a:SubmittedDate/text()')

    @property
    @first_element
    def report_processing_status(self):
        return self.xpath('./a:ReportProcessingStatus/text()')

    @property
    @first_element
    def generated_report_id(self):
        return self.xpath('./a:GeneratedReportId/text()')

    @property
    @parse_date
    @first_element
    def completed_date(self):
        return self.xpath('./a:CompletedDate/text()')

    @property
    @parse_date
    @first_element
    def started_processing_date(self):
        return self.xpath('./a:StartedProcessingDate/text()')

