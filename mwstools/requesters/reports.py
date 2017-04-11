import datetime
import time
import logging

from ..utils import to_amazon_timestamp
from ..parsers.reports import RequestReportResponse, GetReportRequestListResponse
from .base import raise_for_error
from ..mws_overrides import OverrideReports


class ReportFailedError(ValueError):

    def __init__(self, report_request_id, status, *args):
        self.status = status
        self.report_request_id = report_request_id
        self.message = 'GetReportRequestList for report_request_id={} returned {}'.format(self.report_request_id, self.status)
        super(ReportFailedError, self).__init__(self.message, *args)


class ReportRequester(object):
    """
    Request wrapper for a single report.
    """

    def __init__(self, access_key, secret_key, account_id, report_type, region='US', domain='', uri="", version=""):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api = OverrideReports(access_key=access_key, secret_key=secret_key, account_id=account_id,
                                   region=region, domain=domain, uri=uri, version=version)
        self.report_type = report_type

    def _request(self, start_date=None, end_date=None, marketplaceids=()):
        """
        Send request to amazon to request new report for instances report type.

        :param start_date: Begin date range of records to include in the report.
        :param end_date: End date range of records to include in the report.
        :param marketplaceids:
        :return:
        """
        start_date = to_amazon_timestamp(start_date or (datetime.datetime.now() - datetime.timedelta(days=30)))
        end_date = to_amazon_timestamp(end_date or datetime.datetime.now())
        self.logger.debug('requesting {} between {} and {}'.format(self.report_type, start_date, end_date))
        response = self.api.request_report(self.report_type, start_date, end_date, marketplaceids)
        response.raise_for_status()
        return response.content

    def request(self, start_date=None, end_date=None, marketplaceids=()):
        return RequestReportResponse.load(self._request(start_date, end_date, marketplaceids))

    def _get_report_status(self, report_request_id):
        self.logger.debug('getting report request list for request id {}'.format(report_request_id))
        response = self.api.get_report_request_list(requestids=(report_request_id,))
        response.raise_for_status()
        return response.content

    def get_report_status(self, report_request_id):
        doc = self._get_report_status(report_request_id)
        return GetReportRequestListResponse.load(doc)

    def download(self, generated_report_id):
        self.logger.debug('downloading report for report id {}'.format(generated_report_id))
        response = self.api.get_report(generated_report_id)
        return response.content

    def poll(self, report_request_id):
        """
        Wait for report to finish processing and return the generate report id.

        :param report_request_id:
        :return:
        """
        report_status_response = self.get_report_status(report_request_id)
        report_status_info = report_status_response.report_request_info_list()[0]
        status = report_status_info.report_processing_status
        while True:
            self.logger.debug('report_request_id={} report_processing_status={}'.format(report_request_id, status))
            # Completed date is `None` if report isn't finished processing, otherwise it's a datetime object
            done = bool(report_status_info.completed_date)
            if done:
                break
            time.sleep(60)  # Wait a bit for the report status to change

            report_status_response = self.get_report_status(report_request_id)
            report_status_info = report_status_response.report_request_info_list()[0]
            status = report_status_info.report_processing_status

        if status != '_DONE_':
            raise ReportFailedError(report_request_id, status)
        return report_status_info.generated_report_id

    def request_and_download(self, start_date=None, end_date=None, marketplaceids=()):
        """
        request, wait, and download.

        :return:
        """
        requested_report_response = self.request(start_date, end_date, marketplaceids)
        report_id = self.poll(requested_report_response.request_report_result.report_request_id)
        report_contents = self.download(report_id)
        self.api.update_report_acknowledgements(report_ids=(report_id,), acknowledged=True)
        return report_contents
