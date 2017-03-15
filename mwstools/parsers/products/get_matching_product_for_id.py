from ..base import BaseElementWrapper, first_element
from .errors import ProductErrorElement


class GetMatchingProductForIdProduct(BaseElementWrapper):
    namespaces = {
        'a': 'http://mws.amazonservices.com/schema/Products/2011-10-01',
        'b': 'http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd'
    }

    attrs = [
        'asin'
    ]

    @property
    @first_element
    def asin(self):
        return self.xpath('./a:Identifiers/a:MarketplaceASIN/a:ASIN/text()')


class GetMatchingProductForIdResult(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonservices.com/schema/Products/2011-10-01'}

    attrs = [
        'id_',
        'id_type',
        'status',
        'products'
    ]

    @property
    @first_element
    def id_(self):
        return self.xpath('./@Id')

    @property
    @first_element
    def id_type(self):
        return self.xpath('./@IdType')

    @property
    @first_element
    def status(self):
        return self.xpath('./@status')

    def is_success(self):
        return self.status.lower() == 'success'

    def products(self):
        return [GetMatchingProductForIdProduct(x) for x in self.xpath('./a:Products//a:Product')]

    @property
    @first_element
    def _error(self):
        return self.xpath('./a:Error')

    @property
    def error(self):
        e = self._error
        if not e:
            return
        return ProductErrorElement(e, self.id_, self.status)


class GetMatchingProductForIdResponse(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonservices.com/schema/Products/2011-10-01'}
    attrs = [
        'results',
        'request_id'
    ]

    @property
    @first_element
    def request_id(self):
        return self.xpath('./a:ResponseMetadata/a:RequestId/text()')

    def results(self):
        return [GetMatchingProductForIdResult(x) for x in self.xpath('.//a:GetMatchingProductForIdResult')]