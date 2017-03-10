import logging

from ..parsers.products import GetCompetitivePricingForAsinResponse, GetLowestOfferListingsForAsinResponse, GetMatchingProductForIdResponse, GetMyFeesEstimateResponse
from ..requesters.base import raise_response_for_error
from ..mws_overrides import OverrideProducts


class GetCompetitivePricingForAsinRequester(object):

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api = OverrideProducts(*args, **kwargs)

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


class GetMatchingProductForIdRequester(object):

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api = OverrideProducts(*args, **kwargs)

    @raise_response_for_error
    def _request(self, marketplaceid, type='UPC', ids=()):
        response = self.api.get_matching_product_for_id(marketplaceid, type, ids)
        response.raise_for_status()
        return response

    def request(self, marketplaceid, type='UPC', ids=()):
        response = self._request(marketplaceid, type, ids)
        return GetMatchingProductForIdRequester.results_from_response(response)

    @classmethod
    def results_from_response(cls, response):
        gmpfir = GetMatchingProductForIdResponse.load(response.content)
        for result in gmpfir.results():
            yield result


class GetMyFeesEstimateRequester(object):

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api = OverrideProducts(*args, **kwargs)

    def _request(self, marketplaceid, asins=()):
        estimate_requests = [self.api.gen_fees_estimate_request(marketplaceid, a, identifier='request-{}'.format(a)) for a in asins]
        response = self.api.get_my_fees_estimate(estimate_requests)
        response.raise_for_status()
        return response

    def request(self, marketplaceid, asins=()):
        response = self._request(marketplaceid, asins)
        return GetMyFeesEstimateRequester.results_from_response(response)

    @classmethod
    def results_from_response(cls, response):
        gmfer = GetMyFeesEstimateResponse.load(response.content)
        for result in gmfer.fees_estimate_result_list:
            yield result
