from ..base import BaseElementWrapper, first_element

NAMESPACES = {
    'a': 'http://mws.amazonservices.com/schema/Products/2011-10-01'
}


class Offer(BaseElementWrapper):

    namespaces = NAMESPACES

    @property
    @first_element
    def landed_price(self):
        return self.xpath('./a:BuyingPrice/a:LandedPrice/a:Amount/text()')

    @property
    @first_element
    def listing_price(self):
        return self.xpath('./a:BuyingPrice/a:ListingPrice/a:Amount/text()')

    @property
    @first_element
    def shipping(self):
        return self.xpath('./a:BuyingPrice/a:Shipping/a:Amount/text()')

    @property
    @first_element
    def regular_price(self):
        return self.xpath('./a:RegularPrice/a:Amount/text()')

    @property
    @first_element
    def fulfillment_channel(self):
        return self.xpath('./a:FulfillmentChannel/text()')

    @property
    @first_element
    def item_condition(self):
        return self.xpath('./a:ItemCondition/text()')

    @property
    @first_element
    def item_sub_condition(self):
        return self.xpath('./a:ItemSubCondition/text()')

    @property
    @first_element
    def seller_id(self):
        return self.xpath('./a:SellerId/text()')

    @property
    @first_element
    def seller_sku(self):
        return self.xpath('./a:SellerSKU/text()')


class Product(BaseElementWrapper):

    namespaces = NAMESPACES

    @property
    @first_element
    def marketplace_id(self):
        return self.xpath('./a:Identifiers/a:MarketplaceASIN/a:MarketplaceId/text()')

    @property
    @first_element
    def asin(self):
        return self.xpath('./a:Identifiers/a:MarketplaceASIN/a:ASIN/text()')

    @property
    @first_element
    def seller_id(self):
        return self.xpath('./a:Identifiers/a:SKUIdentifier/a:SellerId/text()')

    @property
    @first_element
    def seller_sku(self):
        return self.xpath('./a:Identifiers/a:SKUIdentifier/a:SellerSKU/text()')

    @property
    def offers(self):
        return [Offer(x) for x in self.xpath('./a:Offers/a:Offer')]


class GetMyPriceForSkuResult(BaseElementWrapper):

    namespaces = NAMESPACES

    @property
    @first_element
    def seller_sku(self):
        return self.xpath('./@SellerSKU')

    @property
    @first_element
    def status(self):
        return self.xpath('./@status')

    def is_success(self):
        return self.status == 'Success'

    @property
    @first_element
    def _product(self):
        return self.xpath('./a:Product')

    @property
    def product(self):
        return Product(self._product)


class GetMyPriceForSkuResponse(BaseElementWrapper):

    namespaces = NAMESPACES

    @property
    def get_my_price_for_sku_results(self):
        return [GetMyPriceForSkuResult(x) for x in self.xpath('./a:GetMyPriceForSKUResult')]

    @property
    @first_element
    def request_id(self):
        return self.xpath('./a:ResponseMetadata/a:RequestId/text()')