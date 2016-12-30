import logging

from .utils import write_response
from ..utils import to_amazon_timestamp
from .base import raise_for_error
from ..parsers.orders import ListOrdersResponse, ListOrderItemsResponse
from ..mws_overrides import OverrideOrders


class ListOrdersRequester(object):
    def __init__(self, access_key, secret_key, account_id, region='US', domain='', uri="", version=""):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api = OverrideOrders(access_key, secret_key, account_id, region, domain, uri, version)

    @raise_for_error
    def _request(self, marketplace_ids=('ATVPDKIKX0DER',), created_after=None, created_before=None,
                 last_updated_after=None,
                 last_updated_before=None, order_status=(), fulfillment_channels=(),
                 payment_methods=(), buyer_email=None, seller_order_id=None, max_results=100):
        """
        Wrapper for ListOrders operation.
        See: http://docs.developer.amazonservices.com/en_US/orders/2011-01-01/Orders_ListOrders.html.

        :param created_after:
        :param created_before:
        :param last_updated_after:
        :param last_updated_before:
        :param order_status:
        :param fulfillment_channels:
        :param payment_methods:
        :param buyer_email:
        :param seller_order_id:
        :param max_results:
        :return:
        """
        max_results = str(max_results)
        created_after = to_amazon_timestamp(created_after)
        created_before = to_amazon_timestamp(created_before)
        last_updated_after = to_amazon_timestamp(last_updated_after)
        last_updated_before = to_amazon_timestamp(last_updated_before)
        response = self.api.list_orders(marketplace_ids, created_after, created_before, last_updated_after,
                                        last_updated_before, order_status, fulfillment_channels, payment_methods,
                                        buyer_email, seller_order_id, max_results)
        write_response(response, 'ListOrdersResponse.xml')
        msg = '; '.join('{}={}'.format(k, v) for k, v in response.headers.items())
        self.logger.debug('ResponseHeaders: {}'.format(msg))
        response.raise_for_status()
        return response.content

    def request(self, marketplace_ids=('ATVPDKIKX0DER',), created_after=None, created_before=None,
                last_updated_after=None,
                last_updated_before=None, order_status=(), fulfillment_channels=(),
                payment_methods=(), buyer_email=None, seller_order_id=None, max_results=100):
        return ListOrdersResponse.load(self._request(marketplace_ids, created_after, created_before,
                                                     last_updated_after, last_updated_before, order_status,
                                                     fulfillment_channels,
                                                     payment_methods, buyer_email, seller_order_id, max_results))

    @raise_for_error
    def _request_next_token(self, next_token):
        response = self.api.list_orders_by_next_token(next_token)
        write_response(response, 'ListOrdersResponse.xml')
        response.raise_for_status()
        return response.content

    def from_next_token(self, next_token):
        return ListOrdersResponse.load(self._request_next_token(next_token))


class ListOrderItemsRequester(object):

    def __init__(self, access_key, secret_key, account_id, region='US', domain='', uri="", version=""):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api = OverrideOrders(access_key, secret_key, account_id, region, domain, uri, version)

    @raise_for_error
    def _request(self, amazon_order_id):
        response = self.api.list_order_items(amazon_order_id)
        write_response(response, 'ListOrderItemsResponse.xml')
        msg = '; '.join('{}={}'.format(k, v) for k, v in response.headers.items())
        self.logger.debug('ResponseHeaders: {}'.format(msg))
        response.raise_for_status()
        return response.content

    def request(self, amazon_order_id):
        return ListOrderItemsResponse.load(self._request(amazon_order_id))

    @raise_for_error
    def _request_next_token(self, next_token):
        response = self.api.list_order_items_by_next_token(next_token)
        write_response(response, 'ListOrderItemsResponse.xml')
        response.raise_for_status()
        return response.content

    def from_next_token(self, next_token):
        return ListOrderItemsResponse.load(self._request_next_token(next_token))
