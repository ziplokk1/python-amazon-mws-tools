import urllib

from requests import Session, Response
from requests.adapters import HTTPAdapter, CaseInsensitiveDict, get_encoding_from_headers, extract_cookies_to_jar
from mws.mws import MWS, remove_empty, DictWrapper, DataWrapper, calc_md5

from mwstools.parsers.errors import ErrorResponse

try:
    from xml.etree.ElementTree import ParseError as XMLError
except ImportError:
    from xml.parsers.expat import ExpatError as XMLError


class MWSResponse(Response):

    def raise_for_api_error(self):
        """
        Parse the response content to get an error if exists and raise it.

        :return:
        """
        e = ErrorResponse.load(self.content)
        e.raise_for_error()

    def raise_for_status(self):
        self.raise_for_api_error()
        super(MWSResponse, self).raise_for_status()


class AmazonAdapter(HTTPAdapter):
    """
    Used to apply our custom response class.
    """

    adapter_prefix = 'https://mws.amazonservices.com'

    def build_response(self, req, resp):
        response = MWSResponse()

        # Fallback to None if there's no status_code, for whatever reason.
        response.status_code = getattr(resp, 'status', None)

        # Make headers case-insensitive.
        response.headers = CaseInsensitiveDict(getattr(resp, 'headers', {}))

        # Set encoding.
        response.encoding = get_encoding_from_headers(response.headers)
        response.raw = resp
        response.reason = response.raw.reason

        if isinstance(req.url, bytes):
            response.url = req.url.decode('utf-8')
        else:
            response.url = req.url

        # Add new cookies from the server.
        extract_cookies_to_jar(response.cookies, req, resp)

        # Give the Response some context.
        response.request = req
        response.connection = self

        return response


class _MWS(MWS):
    """
    Override MWS so that there is logic splitting up the request and the parser.

    This way we can catch any request errors that go out and so that the parsers will work properly since they
    have to read the raw xml body.
    """

    def __init__(self, *args, **kwargs):
        session = kwargs.get('session')
        if session:
            kwargs.pop('session')
        else:
            session = Session()
        self.session = session
        self.session.mount(AmazonAdapter.adapter_prefix, AmazonAdapter())
        MWS.__init__(self, *args, **kwargs)

    def request(self, extra_data, method="GET", **kwargs):
        """
        Make request to Amazon MWS API with these parameters
        """

        # Remove all keys with an empty value because
        # Amazon's MWS does not allow such a thing.
        extra_data = remove_empty(extra_data)

        params = {
            'AWSAccessKeyId': self.access_key,
            self.ACCOUNT_TYPE: self.account_id,
            'SignatureVersion': '2',
            'Timestamp': self.get_timestamp(),
            'Version': self.version,
            'SignatureMethod': 'HmacSHA256',
        }
        params.update(extra_data)
        request_description = '&'.join(
            ['%s=%s' % (k, urllib.quote(params[k], safe='-_.~').encode('utf-8')) for k in sorted(params)])
        signature = self.calc_signature(method, request_description)
        url = '%s%s?%s&Signature=%s' % (self.domain, self.uri, request_description, urllib.quote(signature))
        headers = {'User-Agent': 'python-amazon-mws/0.0.1 (Language=Python)'}
        headers.update(kwargs.get('extra_headers', {}))

        return self.session.request(method, url, data=kwargs.get('body', ''), headers=headers)

    def make_request(self, extra_data, method="GET", **kwargs):
        """
        Return dict wrapper from raw request.

        :param extra_data:
        :param method:
        :param kwargs:
        :return:
        """
        response = self.request(extra_data, method, **kwargs)
        try:
            parsed_response = DictWrapper(response.content, extra_data.get("Action") + "Result")
        except XMLError:
            parsed_response = DataWrapper(response.content, response.headers)

        # Store the response object in the parsed_response for quick access
        parsed_response.response = response
        return parsed_response

    def get_service_status(self):
        """
            Returns a GREEN, GREEN_I, YELLOW or RED status.
            Depending on the status/availability of the API its being called from.
        """

        return self.request(extra_data=dict(Action='GetServiceStatus'))


class OverrideFeeds(_MWS):
    """ Amazon MWS Feeds API """

    ACCOUNT_TYPE = "Merchant"

    def submit_feed(self, feed, feed_type, marketplaceids=None,
                    content_type="text/xml", purge=False):
        """
        Uploads a feed ( xml or .tsv ) to the seller's inventory.
        Can be used for creating/updating products on Amazon.
        """
        purge = 'true' if purge else 'false'
        data = dict(Action='SubmitFeed',
                    FeedType=feed_type,
                    PurgeAndReplace=purge)
        data.update(self.enumerate_param('MarketplaceIdList.Id.', marketplaceids))
        md = calc_md5(feed)
        return self.request(data, method="POST", body=feed,
                            extra_headers={'Content-MD5': md, 'Content-Type': content_type})

    def get_feed_submission_list(self, feedids=None, max_count=None, feedtypes=None,
                                 processingstatuses=None, fromdate=None, todate=None):
        """
        Returns a list of all feed submissions submitted in the previous 90 days.
        That match the query parameters.
        """

        data = dict(Action='GetFeedSubmissionList',
                    MaxCount=max_count,
                    SubmittedFromDate=fromdate,
                    SubmittedToDate=todate, )
        data.update(self.enumerate_param('FeedSubmissionIdList.Id', feedids))
        data.update(self.enumerate_param('FeedTypeList.Type.', feedtypes))
        data.update(self.enumerate_param('FeedProcessingStatusList.Status.', processingstatuses))
        return self.request(data)

    def get_submission_list_by_next_token(self, token):
        data = dict(Action='GetFeedSubmissionListByNextToken', NextToken=token)
        return self.request(data)

    def get_feed_submission_count(self, feedtypes=None, processingstatuses=None, fromdate=None, todate=None):
        data = dict(Action='GetFeedSubmissionCount',
                    SubmittedFromDate=fromdate,
                    SubmittedToDate=todate)
        data.update(self.enumerate_param('FeedTypeList.Type.', feedtypes))
        data.update(self.enumerate_param('FeedProcessingStatusList.Status.', processingstatuses))
        return self.request(data)

    def cancel_feed_submissions(self, feedids=None, feedtypes=None, fromdate=None, todate=None):
        data = dict(Action='CancelFeedSubmissions',
                    SubmittedFromDate=fromdate,
                    SubmittedToDate=todate)
        data.update(self.enumerate_param('FeedSubmissionIdList.Id.', feedids))
        data.update(self.enumerate_param('FeedTypeList.Type.', feedtypes))
        return self.request(data)

    def get_feed_submission_result(self, feedid):
        data = dict(Action='GetFeedSubmissionResult', FeedSubmissionId=feedid)
        return self.request(data)


class OverrideOrders(_MWS):
    """
    Return only the request and not the parsed response from all methods in the Orders class from MWS.
    """

    URI = "/Orders/2013-09-01"
    VERSION = "2013-09-01"
    NS = '{https://mws.amazonservices.com/Orders/2013-09-01}'

    def list_orders(self, marketplaceids, created_after=None, created_before=None, lastupdatedafter=None,
                    lastupdatedbefore=None, orderstatus=(), fulfillment_channels=(),
                    payment_methods=(), buyer_email=None, seller_orderid=None, max_results='100'):
        data = dict(Action='ListOrders',
                    CreatedAfter=created_after,
                    CreatedBefore=created_before,
                    LastUpdatedAfter=lastupdatedafter,
                    LastUpdatedBefore=lastupdatedbefore,
                    BuyerEmail=buyer_email,
                    SellerOrderId=seller_orderid,
                    MaxResultsPerPage=max_results,
                    )
        data.update(self.enumerate_param('OrderStatus.Status.', orderstatus))
        data.update(self.enumerate_param('MarketplaceId.Id.', marketplaceids))
        data.update(self.enumerate_param('FulfillmentChannel.Channel.', fulfillment_channels))
        data.update(self.enumerate_param('PaymentMethod.Method.', payment_methods))
        return self.request(data)

    def list_orders_by_next_token(self, token):
        data = dict(Action='ListOrdersByNextToken', NextToken=token)
        return self.request(data)

    def get_order(self, amazon_order_ids):
        data = dict(Action='GetOrder')
        data.update(self.enumerate_param('AmazonOrderId.Id.', amazon_order_ids))
        return self.request(data)

    def list_order_items(self, amazon_order_id):
        data = dict(Action='ListOrderItems', AmazonOrderId=amazon_order_id)
        return self.request(data)

    def list_order_items_by_next_token(self, token):
        data = dict(Action='ListOrderItemsByNextToken', NextToken=token)
        return self.request(data)


class OverrideProducts(_MWS):
    """ Amazon MWS Products API """

    URI = '/Products/2011-10-01'
    VERSION = '2011-10-01'
    NS = '{http://mws.amazonservices.com/schema/Products/2011-10-01}'

    def list_matching_products(self, marketplaceid, query, contextid=None):
        """ Returns a list of products and their attributes, ordered by
            relevancy, based on a search query that you specify.
            Your search query can be a phrase that describes the product
            or it can be a product identifier such as a UPC, EAN, ISBN, or JAN.
        """
        data = dict(Action='ListMatchingProducts',
                    MarketplaceId=marketplaceid,
                    Query=query,
                    QueryContextId=contextid)
        return self.request(data)

    def get_matching_product(self, marketplaceid, asins):
        """ Returns a list of products and their attributes, based on a list of
            ASIN values that you specify.
        """
        data = dict(Action='GetMatchingProduct', MarketplaceId=marketplaceid)
        data.update(self.enumerate_param('ASINList.ASIN.', asins))
        return self.request(data)

    def get_matching_product_for_id(self, marketplaceid, type, ids):
        """ Returns a list of products and their attributes, based on a list of
            product identifier values (ASIN, SellerSKU, UPC, EAN, ISBN, GCID  and JAN)
            The identifier type is case sensitive.
            Added in Fourth Release, API version 2011-10-01
        """
        data = dict(Action='GetMatchingProductForId',
                    MarketplaceId=marketplaceid,
                    IdType=type)
        data.update(self.enumerate_param('IdList.Id.', ids))
        return self.request(data)

    def get_competitive_pricing_for_sku(self, marketplaceid, skus):
        """ Returns the current competitive pricing of a product,
            based on the SellerSKU and MarketplaceId that you specify.
        """
        data = dict(Action='GetCompetitivePricingForSKU', MarketplaceId=marketplaceid)
        data.update(self.enumerate_param('SellerSKUList.SellerSKU.', skus))
        return self.request(data)

    def get_competitive_pricing_for_asin(self, marketplaceid, asins):
        """ Returns the current competitive pricing of a product,
            based on the ASIN and MarketplaceId that you specify.
        """
        data = dict(Action='GetCompetitivePricingForASIN', MarketplaceId=marketplaceid)
        data.update(self.enumerate_param('ASINList.ASIN.', asins))
        return self.request(data)

    def get_lowest_offer_listings_for_sku(self, marketplaceid, skus, condition="Any", excludeme="False"):
        data = dict(Action='GetLowestOfferListingsForSKU',
                    MarketplaceId=marketplaceid,
                    ItemCondition=condition,
                    ExcludeMe=excludeme)
        data.update(self.enumerate_param('SellerSKUList.SellerSKU.', skus))
        return self.request(data)

    def get_lowest_offer_listings_for_asin(self, marketplaceid, asins, condition="Any", excludeme="False"):
        data = dict(Action='GetLowestOfferListingsForASIN',
                    MarketplaceId=marketplaceid,
                    ItemCondition=condition,
                    ExcludeMe=excludeme)
        data.update(self.enumerate_param('ASINList.ASIN.', asins))
        return self.request(data)

    def get_lowest_priced_offers_for_sku(self, marketplaceid, sku, condition="New", excludeme="False"):
        data = dict(Action='GetLowestPricedOffersForSKU',
                    MarketplaceId=marketplaceid,
                    SellerSKU=sku,
                    ItemCondition=condition,
                    ExcludeMe=excludeme)
        return self.request(data)

    def get_lowest_priced_offers_for_asin(self, marketplaceid, asin, condition="New", excludeme="False"):
        data = dict(Action='GetLowestPricedOffersForASIN',
                    MarketplaceId=marketplaceid,
                    ASIN=asin,
                    ItemCondition=condition,
                    ExcludeMe=excludeme)
        return self.request(data)

    def get_product_categories_for_sku(self, marketplaceid, sku):
        data = dict(Action='GetProductCategoriesForSKU',
                    MarketplaceId=marketplaceid,
                    SellerSKU=sku)
        return self.request(data)

    def get_product_categories_for_asin(self, marketplaceid, asin):
        data = dict(Action='GetProductCategoriesForASIN',
                    MarketplaceId=marketplaceid,
                    ASIN=asin)
        return self.request(data)

    def get_my_price_for_sku(self, marketplaceid, skus, condition=None):
        data = dict(Action='GetMyPriceForSKU',
                    MarketplaceId=marketplaceid,
                    ItemCondition=condition)
        data.update(self.enumerate_param('SellerSKUList.SellerSKU.', skus))
        return self.request(data)

    def get_my_price_for_asin(self, marketplaceid, asins, condition=None):
        data = dict(Action='GetMyPriceForASIN',
                    MarketplaceId=marketplaceid,
                    ItemCondition=condition)
        data.update(self.enumerate_param('ASINList.ASIN.', asins))
        return self.request(data)

    def flatten(self, l_key, l_val, d):
        """
        Flatten a dictionary which holds urlparams.

        Used when generating a requests urlparams which have a list.
        Example: GetMyFeesEstimate needs a FeesEstimateRequestList enumerated list parameter.
        :param l_key: List key. The Key to use for the enumeration. ex FeesEstimateRequestList
        :param l_val: List value. The value to use for the enumeration. ex FeesEstimateRequest
        :return: Flattened dictionary which can then be urlencoded to make the signature string.
        """
        nd = {}
        for k, v in d.items():
            if isinstance(v, dict):
                for k_, v_ in v.items():
                    nd[k_] = self.flatten(l_key, l_val, v_)
            elif isinstance(v, list):
                # enumerate the list parameters so that its formatted in the correct way for the url parameters.
                # ex. FeesEstimateRequestList.FeesEstimateRequest.1.IdValue
                # <List Key>.<List Value>.<Enumeration Index>.<Dict Key>
                for i, fee_estimate_request in enumerate(v, 1):
                    for k_, v_ in fee_estimate_request.items():
                        nd['{}.{}.{}.{}'.format(l_key, l_val, i, k_)] = v_
            else:
                nd[k] = v
        return nd

    def fmt_bool(self, b):
        """
        Format boolean to be used with url parameters.
        :param b:
        :return:
        """
        return 'true' if b else 'false'

    def gen_fees_estimate_request(self, marketplace_id, id_value, id_type='ASIN', is_amazon_fulfilled=True,
                                  identifier='request-1', shipping=0.0, listing_price=100.0, currency_code='USD'):
        """
        Generate a fees estimate request element for the url parameters.

        - See http://docs.developer.amazonservices.com/en_US/products/Products_Datatypes.html#FeesEstimateRequest.

        :param marketplace_id: Marketplace ID
        :param id_value: The product identifier.
        :param id_type: The type of product identifier used by IdValue. (ASIN, SellerSKU)
        :param is_amazon_fulfilled: true if the offer is fulfilled by amazon.
        :param identifier: A unique value that will identify this request
        :param shipping: The currency amount for the shipping parameter.
        :param listing_price: The currency amount for the listing price parameter.
        :param currency_code:
        :return: A dict which contains values to be fed into get_my_fees_estimate.
        """

        lp = '%02f' % listing_price
        sp = '%02f' % shipping
        return {
            'MarketplaceId': marketplace_id,
            'IdType': id_type,
            'IdValue': id_value,
            'IsAmazonFulfilled': self.fmt_bool(is_amazon_fulfilled),
            'Identifier': identifier,
            'PriceToEstimateFees.ListingPrice.CurrencyCode': currency_code,
            'PriceToEstimateFees.ListingPrice.Amount': lp,
            'PriceToEstimateFees.Shipping.CurrencyCode': currency_code,
            'PriceToEstimateFees.Shipping.Amount': sp
        }

    def get_my_fees_estimate(self, estimate_requests=()):
        """
        http://docs.developer.amazonservices.com/en_US/products/Products_GetMyFeesEstimate.html

        To use, create your estimate request element first with gen_fees_estimate_request.
        Create a list to hold your generated fees estimate request dicts.
        Pass the list to estimate_requests parameter.

        usage:

        >>> api = OverrideProducts('access_key', 'secret_key', 'account_id')
        >>> asins = ['asin-1', 'asin-2']  # up to 10 asins.
        >>> estimate_requests = [api.gen_fees_estimate_request('marketplace_id', x) for x in asins]
        >>> response = api.get_my_fees_estimate(estimate_requests)
        >>> print response.original

        :param estimate_requests: The list of estimate request dicts.
        :return:
        """
        params = {
            'FeesEstimateRequestList': estimate_requests,
            'Action': 'GetMyFeesEstimate'
        }
        params = self.flatten('FeesEstimateRequestList', 'FeesEstimateRequest', params)
        return self.request(params)


class OverrideReports(_MWS):
    """ Amazon MWS Reports API """

    ACCOUNT_TYPE = "Merchant"

    def get_report(self, report_id):
        data = dict(Action='GetReport', ReportId=report_id)
        return self.request(data)

    def get_report_count(self, report_types=(), acknowledged=None, fromdate=None, todate=None):
        data = dict(Action='GetReportCount',
                    Acknowledged=acknowledged,
                    AvailableFromDate=fromdate,
                    AvailableToDate=todate)
        data.update(self.enumerate_param('ReportTypeList.Type.', report_types))
        return self.request(data)

    def get_report_list(self, requestids=(), max_count=None, types=(), acknowledged=None,
                        fromdate=None, todate=None):
        data = dict(Action='GetReportList',
                    Acknowledged=acknowledged,
                    AvailableFromDate=fromdate,
                    AvailableToDate=todate,
                    MaxCount=max_count)
        data.update(self.enumerate_param('ReportRequestIdList.Id.', requestids))
        data.update(self.enumerate_param('ReportTypeList.Type.', types))
        return self.request(data)

    def get_report_list_by_next_token(self, token):
        data = dict(Action='GetReportListByNextToken', NextToken=token)
        return self.request(data)

    def get_report_request_count(self, report_types=(), processingstatuses=(), fromdate=None, todate=None):
        data = dict(Action='GetReportRequestCount',
                    RequestedFromDate=fromdate,
                    RequestedToDate=todate)
        data.update(self.enumerate_param('ReportTypeList.Type.', report_types))
        data.update(self.enumerate_param('ReportProcessingStatusList.Status.', processingstatuses))
        return self.request(data)

    def get_report_request_list_by_next_token(self, token):
        data = dict(Action='GetReportRequestListByNextToken', NextToken=token)
        return self.request(data)

    def get_report_schedule_list(self, types=()):
        data = dict(Action='GetReportScheduleList')
        data.update(self.enumerate_param('ReportTypeList.Type.', types))
        return self.request(data)

    def get_report_schedule_count(self, types=()):
        data = dict(Action='GetReportScheduleCount')
        data.update(self.enumerate_param('ReportTypeList.Type.', types))
        return self.request(data)

    def update_report_acknowledgements(self, report_ids=(), acknowledged=False):
        data = dict(Action='UpdateReportAcknowledgements', Acknowledged='true' if acknowledged else 'false')
        data.update(self.enumerate_param('ReportIdList.Id.', report_ids))
        return self.request(data)

    def request_report(self, report_type, start_date=None, end_date=None, marketplaceids=()):
        data = dict(Action='RequestReport',
                    ReportType=report_type,
                    StartDate=start_date,
                    EndDate=end_date)
        data.update(self.enumerate_param('MarketplaceIdList.Id.', marketplaceids))
        return self.request(data)

    def get_report_request_list(self, requestids=(), types=(), processingstatuses=(),
                                max_count=None, fromdate=None, todate=None):
        data = dict(Action='GetReportRequestList',
                    MaxCount=max_count,
                    RequestedFromDate=fromdate,
                    RequestedToDate=todate)
        data.update(self.enumerate_param('ReportRequestIdList.Id.', requestids))
        data.update(self.enumerate_param('ReportTypeList.Type.', types))
        data.update(self.enumerate_param('ReportProcessingStatusList.Status.', processingstatuses))
        return self.request(data)
