from ..base import BaseElementWrapper, first_element, parse_bool
from .errors import ProductErrorElement, ProductError
from .base import API_VERSION


class SalesRank(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonservices.com/schema/Products/{}'.format(API_VERSION)}
    attrs = [
        'product_category_id',
        'rank'
    ]

    @property
    @first_element
    def product_category_id(self):
        return self.xpath('./a:ProductCategoryId/text()')

    @property
    @first_element
    def rank(self):
        return self.xpath('./a:Rank/text()')


class OfferListingCount(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonservices.com/schema/Products/{}'.format(API_VERSION)}
    attrs = [
        'condition',
        'count'
    ]

    @property
    @first_element
    def condition(self):
        return self.xpath('./@condition')

    @property
    @first_element
    def count(self):
        return self.xpath('./text()')


class CompetitivePrice(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonservices.com/schema/Products/{}'.format(API_VERSION)}
    attrs = [
        'belongs_to_requester',
        'condition',
        'sub_condition',
        'competitive_price_id',
        'landed_price',
        'listing_price',
        'shipping'
    ]

    @property
    @parse_bool
    @first_element
    def belongs_to_requester(self):
        return self.xpath('./@belongsToRequester')

    @property
    @first_element
    def condition(self):
        return self.xpath('./@condition')

    @property
    @first_element
    def sub_condition(self):
        return self.xpath('./@subcondition')

    @property
    @first_element
    def competitive_price_id(self):
        return self.xpath('./a:CompetitivePriceId/text()')

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


class Product(BaseElementWrapper):
    """
    Wrap the GetCompetitivePricingForASINResult and Product element into one since the only child element
    that GetCompetitivePricingForASINResult has is the Product.
    """

    namespaces = {'a': 'http://mws.amazonservices.com/schema/Products/{}'.format(API_VERSION)}
    attrs = [
        'asin',
        'status',
        'product',
        'marketplace_id',
        'error',
        'competitive_prices',
        'number_of_offer_listings',
        'sales_rankings'
    ]

    @property
    @first_element
    def asin(self):
        return self.xpath('./@ASIN')

    @property
    @first_element
    def status(self):
        return self.xpath('./@status')

    @property
    @first_element
    def _product(self):
        return self.xpath('./a:Product')

    @property
    @first_element
    def _error(self):
        e = self.xpath('./a:Error')
        return e

    @property
    def product(self):
        bew = BaseElementWrapper(self._product)
        bew.set_namespace(self.namespaces)
        return bew

    @property
    @first_element
    def marketplace_id(self):
        return self.product.xpath('./a:Identifiers/a:MarketplaceASIN/a:MarketplaceId/text()')

    @property
    def error(self):
        if self._error is not None:
            return ProductErrorElement(self._error, self.asin, self.status)
        return None

    def competitive_prices(self):
        return [CompetitivePrice(x) for x in self.product.xpath('./a:CompetitivePricing/a:CompetitivePrices//a:CompetitivePrice')]

    def number_of_offer_listings(self):
        return [OfferListingCount(x) for x in self.product.xpath('./a:CompetitivePricing/a:NumberOfOfferListings//a:OfferListingCount')]

    def number_of_new_offer_listings(self):
        l = filter(lambda x: x.condition.lower() == 'new', self.number_of_offer_listings())
        if not l:
            return
        return l[0].count

    def sales_rankings(self):
        return [SalesRank(x) for x in self.product.xpath('./a:SalesRankings//a:SalesRank')]

    def _website_sales_rank_element(self):
        l = filter(lambda x: 'display_on_website' in x.product_category_id, self.sales_rankings())
        if not l:
            return None, None
        return l[0].product_category_id, l[0].rank

    def website_ranking(self):
        return self._website_sales_rank_element()[1]

    def website_category(self):
        return self._website_sales_rank_element()[0]

    def is_success(self):
        return self.status == 'Success'

    def new_landed_price(self):
        l = filter(lambda x: x.condition == 'New' and x.sub_condition == 'New', self.competitive_prices())
        if l:
            new_price = l[0].landed_price
        else:
            new_price = None
        return new_price

    def raise_for_error(self):
        if self.error:
            raise ProductError(self.error.type, self.error.code, self.error.message, self.asin, self.status)

    def __repr__(self):
        return '<{} asin={} status={} price={} rank={}>'.format(
            self.__class__.__name__,
            self.asin,
            self.status,
            self.new_landed_price(),
            self.website_ranking()
        )


class GetCompetitivePricingForAsinResponse(BaseElementWrapper):

    namespaces = {'a': 'http://mws.amazonservices.com/schema/Products/{}'.format(API_VERSION)}
    attrs = [
        'request_id',
        'products'
    ]

    @property
    @first_element
    def request_id(self):
        return self.xpath('./a:ResponseMetadata/a:RequestId/text()')

    def products(self):
        return [Product(x) for x in self.xpath('.//a:GetCompetitivePricingForASINResult')]