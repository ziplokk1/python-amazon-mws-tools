import logging

from ..parsers.products import GetCompetitivePricingForAsinResponse, GetLowestOfferListingsForAsinResponse
from ..requesters.base import raise_response_for_error
from ..mws_overrides import OverrideProducts


class GetCompetitivePricingForAsinRequester(object):

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api = OverrideProducts(*args, **kwargs)

    @raise_response_for_error
    def _request(self, marketplaceid, asins):
        response = self.api.get_competitive_pricing_for_asin(marketplaceid, asins)
        response.raise_for_status()
        return response

    def request(self, marketplaceid, asins):
        response = self._request(marketplaceid, asins)
        return GetCompetitivePricingForAsinRequester.products_from_response(response)

    @staticmethod
    def products_from_response(response):
        p = GetCompetitivePricingForAsinResponse.load(response.content)
        for product in p.products():
            yield product


class GetLowestOfferListingsForAsinRequester(object):

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api = OverrideProducts(*args, **kwargs)

    @raise_response_for_error
    def _request(self, marketplaceid, asins, condition='Any', excludeme=False):
        excludeme = 'True' if excludeme else 'False'
        response = self.api.get_lowest_offer_listings_for_asin(marketplaceid, asins, condition, excludeme)
        response.raise_for_status()
        return response

    def request(self, marketplaceid, asins, condition='Any', excludeme=False):
        response = self._request(marketplaceid, asins, condition, excludeme)
        return GetLowestOfferListingsForAsinResponse.load(response.content)
