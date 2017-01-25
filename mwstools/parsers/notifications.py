from .base import BaseElementWrapper, first_element, parse_date, parse_bool


class SalesRank(BaseElementWrapper):

    attrs = [
        'product_category_id',
        'rank'
    ]

    @property
    @first_element
    def product_category_id(self):
        return self.xpath('./ProductCategoryId/text()')

    @property
    @first_element
    def rank(self):
        return self.xpath('./Rank/text()')


class OfferChangeTrigger(BaseElementWrapper):

    @property
    @first_element
    def marketplace_id(self):
        return self.xpath('./MarketplaceId/text()')

    @property
    @first_element
    def asin(self):
        return self.xpath('./ASIN/text()')

    @property
    @first_element
    def item_condition(self):
        return self.xpath('./ItemCondition/text()')

    @property
    @parse_date
    @first_element
    def time_of_offer_change(self):
        return self.xpath('./TimeOfOfferChange/text()')


class OfferCount(BaseElementWrapper):

    @property
    @first_element
    def condition(self):
        return self.xpath('./@condition')

    @property
    @first_element
    def fulfillment_channel(self):
        return self.xpath('./@fulfillmentChannel')

    @property
    @first_element
    def count(self):
        return self.xpath('./text()')


class LowestPrice(BaseElementWrapper):

    @property
    @first_element
    def condition(self):
        return self.xpath('./@condition')

    @property
    @first_element
    def fulfillment_channel(self):
        return self.xpath('./@fulfillmentChannel')

    @property
    @first_element
    def landed_price(self):
        return self.xpath('./LandedPrice/Amount/text()')

    @property
    @first_element
    def listing_price(self):
        return self.xpath('./ListingPrice/Amount/text()')

    @property
    @first_element
    def shipping(self):
        return self.xpath('./Shipping/Amount/text()')


class BuyBoxPrice(BaseElementWrapper):

    @property
    @first_element
    def condition(self):
        return self.xpath('./@condition')

    @property
    @first_element
    def landed_price(self):
        return self.xpath('./LandedPrice/Amount/text()')

    @property
    @first_element
    def listing_price(self):
        return self.xpath('./ListingPrice/Amount/text()')

    @property
    @first_element
    def shipping(self):
        return self.xpath('./Shipping/Amount/text()')


class Summary(BaseElementWrapper):

    @property
    def number_of_offers(self):
        return [OfferCount(x) for x in self.xpath('./NumberOfOffers//OfferCount')]

    @property
    def buybox_prices(self):
        return [BuyBoxPrice(x) for x in self.xpath('./BuyBoxPrices//BuyBoxPrice')]

    @property
    def sales_rankings(self):
        return [SalesRank(x) for x in self.xpath('./SalesRankings//SalesRank')]

    @property
    def lowest_prices(self):
        return [LowestPrice(x) for x in self.xpath('./LowestPrices//LowestPrice')]

    # ToDo: Buybox eligible offers


class Offer(BaseElementWrapper):

    @property
    @first_element
    def seller_id(self):
        return self.xpath('./SellerId/text()')

    @property
    @first_element
    def subcondition(self):
        return self.xpath('./SubCondition/text()')

    @property
    @first_element
    def seller_positive_feedback_rating(self):
        return self.xpath('./SellerFeedbackRating/SellerPositiveFeedbackRating/text()')

    @property
    @first_element
    def feedback_count(self):
        return self.xpath('./SellerFeedbackRating/FeedbackCount/text()')

    @property
    @first_element
    def shipping_minimum_hours(self):
        return self.xpath('./ShippingTime/@minimumHours')

    @property
    @first_element
    def shipping_maximum_hours(self):
        return self.xpath('./ShippingTime/@maximumHours')

    @property
    @first_element
    def shipping_availability_type(self):
        return self.xpath('./ShippingTime/@availabilityType')

    @property
    @first_element
    def listing_price(self):
        return self.xpath('./ListingPrice/Amount/text()')

    @property
    @first_element
    def shipping(self):
        return self.xpath('./Shipping/Amount/text()')

    def calculated_landed_price(self):
        l = self.listing_price
        s = self.shipping
        if not l or not s:
            return
        try:
            return float(l) + float(s)
        except (TypeError, ValueError):
            return

    @property
    @parse_bool
    @first_element
    def is_fba(self):
        return self.xpath('./IsFulfilledByAmazon/text()')

    @property
    @parse_bool
    @first_element
    def is_buybox_winner(self):
        return self.xpath('./IsBuyBoxWinner/text()')

    @property
    @parse_bool
    @first_element
    def is_featured_merchant(self):
        return self.xpath('./IsFeaturedMerchant/text()')

    @property
    @parse_bool
    @first_element
    def ships_domestically(self):
        return self.xpath('./ShipsDomestically/text()')


class AnyOfferChangedNotification(BaseElementWrapper):

    summary_parser = Summary
    offer_change_trigger_parser = OfferChangeTrigger
    offer_parser = Offer

    @property
    def offer_change_trigger(self):
        l = [self.offer_change_trigger_parser(x) for x in self.xpath('./OfferChangeTrigger')]
        if not l:
            return self.offer_change_trigger_parser(None)
        return l[0]

    @property
    def summary(self):
        l = [self.summary_parser(x) for x in self.xpath('./Summary')]
        if not l:
            return self.summary_parser(None)
        return l[0]

    @property
    def offers(self):
        return [self.offer_parser(x) for x in self.xpath('./Offers//Offer')]


class NotificationMetadata(BaseElementWrapper):

    attrs = [
        'notification_type',
        'payload_version',
        'unique_id',
        'publish_time',
        'seller_id',
        'marketplace_id'
    ]

    @property
    @first_element
    def notification_type(self):
        return self.xpath('./NotificationType/text()')

    @property
    @first_element
    def payload_version(self):
        return self.xpath('./PayloadVersion/text()')

    @property
    @first_element
    def unique_id(self):
        return self.xpath('./UniqueId/text()')

    @property
    @parse_date
    @first_element
    def publish_time(self):
        return self.xpath('./PublishTime/text()')

    @property
    @first_element
    def seller_id(self):
        return self.xpath('./SellerId/text()')

    @property
    @first_element
    def marketplace_id(self):
        return self.xpath('./MarketplaceId/text()')


class NotificationPayload(BaseElementWrapper):

    def __init__(self, *args, **kwargs):
        self.PayloadClass = kwargs.pop('payload_class')
        BaseElementWrapper.__init__(self, *args, **kwargs)

    @property
    def payload(self):
        x = self.xpath('./*')
        if not x:
            return self.PayloadClass(None)
        return self.PayloadClass(x[0])


class Notification(BaseElementWrapper):

    @property
    def notification_metadata(self):
        x = self.xpath('./NotificationMetaData')
        if not x:
            return NotificationMetadata(None)
        return NotificationMetadata(x[0])

    def notification_payload(self, payload_class):
        x = self.xpath('./NotificationPayload')
        if not x:
            return NotificationPayload(None, BaseElementWrapper).payload
        return NotificationPayload(x[0], payload_class=payload_class).payload
