from .base import BaseElementWrapper, first_element, parse_date


class GetServiceStatusResponse(BaseElementWrapper):

    namespaces = {
        'a': 'http://mws.amazonservices.com/schema/Products/2011-10-01'
    }

    attrs = {
        'status',
        'timestamp',
        'request_id'
    }

    @property
    @first_element
    def status(self):
        return self.xpath('./a:GetServiceStatusResult/a:Status/text()')

    @property
    @parse_date
    @first_element
    def timestamp(self):
        return self.xpath('./a:GetServiceStatusResult/a:Timestamp/text()')

    @property
    @first_element
    def request_id(self):
        return self.xpath('./a:ResponseMetadata/a:RequestId/text()')

    def __repr__(self):
        return '<{} status={} timestamp={} request_id={}>'.format(
            self.__class__.__name__,
            self.status,
            self.timestamp,
            self.request_id
        )
