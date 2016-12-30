import logging

from ..parsers.products import GetCompetitivePricingForAsinResponse
from ..requesters.base import raise_for_error
from ..requesters.utils import write_response
from ..mws_overrides import OverrideProducts


class GetCompetitivePricingForAsinRequester(object):

    def __init__(self, access_key, secret_key, account_id,
                 region='US', domain='', uri='', version=''):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api = OverrideProducts(access_key, secret_key, account_id, region, domain, uri, version)

    @raise_for_error
    def _request(self, asins, marketplaceid):
        response = self.api.get_competitive_pricing_for_asin(asins, marketplaceid)
        write_response(response, 'GetCompetitivePricingForAsinResponse.xml')
        response.raise_for_status()
        return response.content

    def request(self, asins, marketplaceid):
        response = self._request(asins, marketplaceid)
        p = GetCompetitivePricingForAsinResponse.load(response)
        for product in p.products():
            yield product

