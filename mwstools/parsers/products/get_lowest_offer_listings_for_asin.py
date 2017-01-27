from .base import API_VERSION
from ..base import BaseElementWrapper, first_element, parse_bool


class LowestOfferListing(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonservices.com/schema/Products/{}'.format(API_VERSION)}
    attrs = [
        'item_condition',
        'item_subcondition',
        'fulfillment_channel',
        'is_fba',
        'ships_domestically',
        'shipping_time_max',
        'seller_positive_feedback_rating',
        'number_of_offer_listings_considered',
        'seller_feedback_count',
        'currency_code',
        'landed_price',
        'listing_price',
        'shipping',
        'multiple_offers_at_lowest_price'
    ]

    @property
    @first_element
    def item_condition(self):
        return self.xpath('./a:Qualifiers/a:ItemCondition/text()')

    @property
    @first_element
    def item_subcondition(self):
        return self.xpath('./a:Qualifiers/a:ItemSubcondition/text()')

    @property
    @first_element
    def fulfillment_channel(self):
        return self.xpath('./a:Qualifiers/a:FulfillmentChannel/text()')

    def is_fba(self):
        return self.fulfillment_channel == 'Amazon'

    @property
    @first_element
    def ships_domestically(self):
        return self.xpath('./a:Qualifiers/a:ShipsDomestically/text()')

    @property
    @first_element
    def shipping_time_max(self):
        return self.xpath('./a:Qualifiers/a:ShippingTime/a:Max/text()')

    @property
    @first_element
    def seller_positive_feedback_rating(self):
        return self.xpath('./a:Qualifiers/a:SellerPositiveFeedbackRating/text()')

    @property
    @first_element
    def number_of_offer_listings_considered(self):
        return self.xpath('./a:NumberOfOfferListingsConsidered/text()')

    @property
    @first_element
    def seller_feedback_count(self):
        return self.xpath('./a:SellerFeedbackCount/text()')

    @property
    @first_element
    def currency_code(self):
        return self.xpath('./a:Price/a:LandedPrice/a:CurrencyCode/text()')

    @property
    @first_element
    def landed_price(self):
        return self.xpath('./a:Price/a:LandedPrice/a:Amount/text()')

    @property
    @first_element
    def listing_price(self):
        return self.xpath('./a:Price/a:ListingPrice/a:Amount/text()')

    @property
    @first_element
    def shipping(self):
        return self.xpath('./a:Price/a:Shipping/a:Amount/text()')

    @property
    @parse_bool
    @first_element
    def multiple_offers_at_lowest_price(self):
        return self.xpath('./a:MultipleOffersAtLowestPrice/text()')

    def __repr__(self):
        return '<{} item_condition={} fulfillment_channel={} landed_price={}>'.format(
            self.__class__.__name__,
            self.item_condition,
            self.fulfillment_channel,
            self.landed_price
        )


class LowestOfferListingProduct(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonservices.com/schema/Products/{}'.format(API_VERSION)}
    attrs = [
        'asin',
        'marketplace_id',
        'lowest_offer_listings'
    ]

    @property
    @first_element
    def asin(self):
        return self.xpath('./a:Identifiers/a:MarketplaceASIN/a:ASIN/text()')

    @property
    @first_element
    def marketplace_id(self):
        return self.xpath('./a:Identifiers/a:MarketplaceASIN/a:MarketplaceId/text()')

    def lowest_offer_listings(self):
        return [LowestOfferListing(x) for x in self.xpath('./a:LowestOfferListings//a:LowestOfferListing')]


class GetLowestOfferListingsForAsinResult(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonservices.com/schema/Products/{}'.format(API_VERSION)}
    attrs = [
        'asin',
        'status',
        'all_offer_listings_considered',
        'is_successful'
    ]

    @property
    @first_element
    def asin(self):
        return self.xpath('./@ASIN')

    @property
    @first_element
    def status(self):
        return self.xpath('./@status')

    def is_successful(self):
        return self.status == 'Success'

    @property
    @parse_bool
    @first_element
    def all_offer_listings_considered(self):
        return self.xpath('./a:AllOfferListingsConsidered/text()')

    @property
    @first_element
    def _product(self):
        return self.xpath('./a:Product')

    def product(self):
        return LowestOfferListingProduct(self._product)


class GetLowestOfferListingsForAsinResponse(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonservices.com/schema/Products/{}'.format(API_VERSION)}
    attrs = [
        'request_id',
        'lowest_offer_listings'
    ]

    @property
    @first_element
    def request_id(self):
        return self.xpath('./a:ResponseMetadata/a:RequestId/text()')

    def lowest_offer_listings_result(self):
        return [GetLowestOfferListingsForAsinResult(x) for x in self.xpath('.//a:GetLowestOfferListingsForASINResult')]