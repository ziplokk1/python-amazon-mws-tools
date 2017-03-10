from ..base import BaseElementWrapper, first_element, parse_bool, parse_date
from .errors import FeesError, ProductErrorElement


class FeeDetail(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonservices.com/schema/Products/2011-10-01'}

    attrs = [
        'fee_amount',
        'final_fee',
        'fee_promotion',
        'fee_type',
        'included_fee_detail_list'
    ]

    def __repr__(self):
        return '<{} fee_type={} fee_amount={} final_fee={} included_detail_list={}>'.format(
            self.__class__.__name__,
            self.fee_type,
            self.fee_amount,
            self.final_fee,
            self.included_fee_detail_list
        )

    @property
    @first_element
    def fee_amount(self):
        return self.xpath('./a:FeeAmount/a:Amount/text()')

    @property
    @first_element
    def final_fee(self):
        return self.xpath('./a:FinalFee/a:Amount/text()')

    @property
    @first_element
    def fee_promotion(self):
        return self.xpath('./a:FeePromotion/a:Amount/text()')

    @property
    @first_element
    def fee_type(self):
        return self.xpath('./a:FeeType/text()')

    @property
    def included_fee_detail_list(self):
        return [FeeDetail(x) for x in self.xpath('./a:IncludedFeeDetailList//a:FeeDetail')]


class FeesEstimateResult(BaseElementWrapper):
    namespaces = {'a': 'http://mws.amazonservices.com/schema/Products/2011-10-01'}

    attrs = [
        'status',
        'is_success',
        'marketplace_id',
        'id_type',
        'seller_id',
        'is_fba',
        'seller_input_identifier',
        'id_value',
        'listing_price',
        'shipping',
        'fee_detail_list',
        'total_fees_estimate',
        'time_of_fees_estimation'
    ]

    def __repr__(self):
        return '<{} id_value={} id_type={} total_fees_estimate={}>'.format(
            self.__class__.__name__,
            self.id_value,
            self.id_type,
            self.total_fees_estimate
        )

    @property
    @first_element
    def status(self):
        return self.xpath('./a:Status/text()')

    def is_success(self):
        return self.status == 'Success'

    @property
    @first_element
    def marketplace_id(self):
        return self.xpath('./a:FeesEstimateIdentifier/a:MarketplaceId/text()')

    @property
    @first_element
    def id_type(self):
        return self.xpath('./a:FeesEstimateIdentifier/a:IdType/text()')

    @property
    @first_element
    def seller_id(self):
        return self.xpath('./a:FeesEstimateIdentifier/a:SellerId/text()')

    @property
    @parse_bool
    @first_element
    def is_fba(self):
        return self.xpath('./a:FeesEstimateIdentifier/a:IsAmazonFulfilled/text()')

    @property
    @first_element
    def seller_input_identifier(self):
        return self.xpath('./a:FeesEstimateIdentifier/a:SellerInputIdentifier/text()')

    @property
    @first_element
    def id_value(self):
        return self.xpath('./a:FeesEstimateIdentifier/a:IdValue/text()')

    @property
    @first_element
    def listing_price(self):
        return self.xpath('./a:FeesEstimateIdentifier/a:PriceToEstimateFees/a:ListingPrice/a:Amount/text()')

    @property
    @first_element
    def shipping(self):
        return self.xpath('./a:FeesEstimateIdentifier/a:PriceToEstimateFees/a:Shipping/a:Amount/text()')

    @property
    def fee_detail_list(self):
        return [FeeDetail(x) for x in self.xpath('./a:FeesEstimate/a:FeeDetailList//a:FeeDetail')]

    @property
    @first_element
    def total_fees_estimate(self):
        return self.xpath('./a:FeesEstimate/a:TotalFeesEstimate/a:Amount/text()')

    @property
    @parse_date
    @first_element
    def time_of_fees_estimation(self):
        return self.xpath('./a:FeesEstimate/a:TimeOfFeesEstimation/text()')

    @property
    @first_element
    def _error(self):
        return self.xpath('./a:Error')

    @property
    def error(self):
        return ProductErrorElement(self._error, self.id_value, self.status)

    def as_error(self):
        return FeesError(self.error.type, self.error.code, self.error.message, self.id_value, self.status)


class GetMyFeesEstimateResponse(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonservices.com/schema/Products/2011-10-01'}
    attrs = [
        'request_id',
        'fees_estimate_result_list'
    ]

    def __repr__(self):
        return '<{} request_id={} fees_estimate_result_list={}>'.format(
            self.__class__.__name__,
            self.request_id,
            self.fees_estimate_result_list
        )

    @property
    @first_element
    def request_id(self):
        return self.xpath('./a:ResponseMetadata/a:RequestId/text()')

    @property
    def fees_estimate_result_list(self):
        return [FeesEstimateResult(x) for x in self.xpath('./a:GetMyFeesEstimateResult/a:FeesEstimateResultList//a:FeesEstimateResult')]
