import re

from .base import first_element, BaseElementWrapper, parse_bool, parse_date


API_VERSION = '2013-09-01'


class OrderItem(BaseElementWrapper):
    
    namespaces = {
        'a': 'https://mws.amazonservices.com/Orders/{}'.format(API_VERSION)
    }

    attrs = [
        'quantity_ordered',
        'title',
        'promotion_discount',
        'currency_code',
        'asin',
        'seller_sku',
        'order_item_id',
        'quantity_shipped',
        'item_price',
        'item_tax'
    ]

    def __init__(self, element, amazon_order_id):
        BaseElementWrapper.__init__(self, element)
        self.amazon_order_id = amazon_order_id

    @property
    @first_element
    def quantity_ordered(self):
        return self.xpath('./a:QuantityOrdered/text()')

    @property
    @first_element
    def title(self):
        return self.xpath('./a:Title/text()')

    @property
    @first_element
    def promotion_discount(self):
        return self.xpath('./a:PromotionDiscount/a:Amount/text()')

    @property
    @first_element
    def currency_code(self):
        return self.xpath('./a:PromotionDiscount/a:CurrencyCode/text()')

    @property
    @first_element
    def asin(self):
        return self.xpath('./a:ASIN/text()')

    @property
    @first_element
    def seller_sku(self):
        return self.xpath('./a:SellerSKU/text()')

    @property
    @first_element
    def order_item_id(self):
        return self.xpath('./a:OrderItemId/text()')

    @property
    @first_element
    def quantity_shipped(self):
        return self.xpath('./a:QuantityShipped/text()')

    @property
    @first_element
    def item_price(self):
        return self.xpath('./a:ItemPrice/a:Amount/text()')

    @property
    @first_element
    def item_tax(self):
        return self.xpath('./a:ItemTax/a:Amount/text()')

    @classmethod
    def load(cls, string, amazon_order_id):
        return cls(cls.string_to_element(string), amazon_order_id)


class ListOrderItemsResponse(BaseElementWrapper):
    
    namespaces = {
        'a': 'https://mws.amazonservices.com/Orders/{}'.format(API_VERSION)
    }
    attrs = [
        'next_token',
        'amazon_order_id',
        'order_items',
        'request_id'
    ]

    def has_next(self):
        return bool(self.next_token)

    @property
    @first_element
    def next_token(self):
        return self.xpath('//a:NextToken/text()')

    @property
    @first_element
    def amazon_order_id(self):
        return self.xpath('./a:ListOrderItemsResult/a:AmazonOrderId/text()')

    def order_items(self):
        return [OrderItem(x, self.amazon_order_id) for x in self.xpath('./a:ListOrderItemsResult//a:OrderItem')]

    @property
    @first_element
    def request_id(self):
        return self.xpath('./a:ResponseMetadata/a:RequestId/text()')


def mk_ship_state(state_value):
    """
    Converts customer supplied state to the uniform state abbreviation
    :param state_value: customer supplied state
    :return: uppercase state abbreviation
    """
    # When order is cancelled, not all the data is in the report, so we account for null states here
    if not state_value:
        return
    states = {"AL": "Alabama",
              "AK": "Alaska",
              "AZ": "Arizona",
              "AR": "Arkansas",
              "CA": "California",
              "CO": "Colorado",
              "CT": "Connecticut",
              "DE": "Delaware",
              "DC": "District of Columbia",
              "FL": "Florida",
              "GA": "Georgia",
              "HI": 'Hawaii',
              "ID": "Idaho",
              "IL": "Illinois",
              "IN": "Indiana",
              "IA": "Iowa",
              "KS": "Kansas",
              "KY": "Kentucky",
              "LA": "Louisiana",
              "ME": "Maine",
              "MD": "Maryland",
              "MA": "Massachusetts",
              "MI": "Michigan",
              "MN": "Minnesota",
              "MS": "Mississippi",
              "MO": "Missouri",
              "MT": "Montana",
              "NE": "Nebraska",
              "NV": "Nevada",
              "NH": "New Hampshire",
              "NJ": "New Jersey",
              "NM": "New Mexico",
              "NY": "New York",
              "NC": "North Carolina",
              "ND": "North Dakota",
              "OH": "Ohio",
              "OK": "Oklahoma",
              "OR": "Oregon",
              "PA": "Pennsylvania",
              "RI": "Rhode Island",
              "SC": "South Carolina",
              "SD": "South Dakota",
              "TN": "Tennessee",
              "TX": "Texas",
              "UT": "Utah",
              "VT": "Vermont",
              "VA": "Virginia",
              "WA": "Washington",
              "WV": "West Virginia",
              "WI": "Wisconsin",
              "WY": "Wyoming"}
    states = {re.sub('\W', '', k).lower(): re.sub('\W', '', v).lower() for k, v in states.items()}
    inverted_states = {v: k for k, v in states.items()}
    sv = re.sub('\W', '', state_value).lower()

    if sv in states:
        return sv.upper()
    elif sv in inverted_states:
        return inverted_states[sv].upper()
    else:
        return state_value
    
    
class Order(BaseElementWrapper):

    namespaces = {
        'a': 'https://mws.amazonservices.com/Orders/{}'.format(API_VERSION)
    }
    attrs = [
        'latest_ship_date',
        'order_type',
        'purchase_date',
        'buyer_email',
        'amazon_order_id',
        'last_update_date',
        'number_of_items_shipped',
        'ship_service_level',
        'order_status',
        'sales_channel',
        'is_business_order',
        'number_of_items_unshipped',
        'buyer_name',
        'currency_code',
        'order_total',
        'is_premium_order',
        'earliest_ship_date',
        'marketplace_id',
        'fulfillment_channel',
        'payment_method',
        'is_prime',
        'shipment_service_level_category',
        'seller_order_id',
        'state_or_region',
        'ship_state_abbreviation',
        'city',
        'phone',
        'country_code',
        'postal_code',
        'name',
        'address_line_1',
        'address_line_2'
    ]

    @property
    @parse_date
    @first_element
    def latest_ship_date(self):
        return self.xpath('./a:LatestShipDate/text()')

    @property
    @first_element
    def order_type(self):
        return self.xpath('./a:OrderType/text()')

    @property
    @parse_date
    @first_element
    def purchase_date(self):
        return self.xpath('./a:PurchaseDate/text()')

    @property
    @first_element
    def buyer_email(self):
        return self.xpath('./a:BuyerEmail/text()')

    @property
    @first_element
    def amazon_order_id(self):
        return self.xpath('./a:AmazonOrderId/text()')

    @property
    @parse_date
    @first_element
    def last_update_date(self):
        return self.xpath('./a:LastUpdateDate/text()')

    @property
    @first_element
    def number_of_items_shipped(self):
        return self.xpath('./a:NumberOfItemsShipped/text()')

    @property
    @first_element
    def ship_service_level(self):
        return self.xpath('./a:ShipServiceLevel/text()')

    @property
    @first_element
    def order_status(self):
        return self.xpath('./a:OrderStatus/text()')

    @property
    @first_element
    def sales_channel(self):
        return self.xpath('./a:SalesChannel/text()')

    @property
    @parse_bool
    @first_element
    def is_business_order(self):
        return self.xpath('./a:IsBusinessOrder/text()')

    @property
    @first_element
    def number_of_items_unshipped(self):
        return self.xpath('./a:NumberOfItemsUnshipped/text()')

    @property
    @first_element
    def buyer_name(self):
        return self.xpath('./a:BuyerName/text()')

    @property
    @first_element
    def currency_code(self):
        return self.xpath('./a:OrderTotal/a:CurrencyCode/text()')

    @property
    @first_element
    def order_total(self):
        return self.xpath('./a:OrderTotal/a:Amount/text()')

    @property
    @parse_bool
    @first_element
    def is_premium_order(self):
        return self.xpath('./a:IsPremiumOrder/text()')

    @property
    @parse_date
    @first_element
    def earliest_ship_date(self):
        return self.xpath('./a:EarliestShipDate/text()')

    @property
    @first_element
    def marketplace_id(self):
        return self.xpath('./a:MarketplaceId/text()')

    @property
    @first_element
    def fulfillment_channel(self):
        return self.xpath('./a:FulfillmentChannel/text()')

    @property
    @first_element
    def payment_method(self):
        return self.xpath('./a:PaymentMethod/text()')

    @property
    @parse_bool
    @first_element
    def is_prime(self):
        return self.xpath('./a:IsPrime/text()')

    @property
    @first_element
    def shipment_service_level_category(self):
        return self.xpath('./a:ShipmentServiceLevelCategory/text()')

    @property
    @first_element
    def seller_order_id(self):
        return self.xpath('./a:SellerOrderId/text()')

    # Address Stuff

    @property
    @first_element
    def state_or_region(self):
        return self.xpath('./a:ShippingAddress/a:StateOrRegion/text()')

    @property
    def ship_state_abbreviation(self):
        """
        Convert the value in state_or_region to a state abbreviation. (ex. Massachusets -> MA)
        :return:
        """
        if self.state_or_region:
            return mk_ship_state(self.state_or_region)
        return

    @property
    @first_element
    def city(self):
        return self.xpath('./a:ShippingAddress/a:City/text()')

    @property
    @first_element
    def phone(self):
        return self.xpath('./a:ShippingAddress/a:Phone/text()')

    @property
    @first_element
    def country_code(self):
        return self.xpath('./a:ShippingAddress/a:CountryCode/text()')

    @property
    @first_element
    def postal_code(self):
        return self.xpath('./a:ShippingAddress/a:PostalCode/text()')

    @property
    @first_element
    def name(self):
        return self.xpath('./a:ShippingAddress/a:Name/text()')

    @property
    @first_element
    def address_line_1(self):
        return self.xpath('./a:ShippingAddress/a:AddressLine1/text()')

    @property
    @first_element
    def address_line_2(self):
        return self.xpath('./a:ShippingAddress/a:AddressLine2/text()')


class ListOrdersResult(BaseElementWrapper):

    namespaces = {
        'a': 'https://mws.amazonservices.com/Orders/{}'.format(API_VERSION)
    }
    attrs = [
        'last_updated_before',
        'next_token',
        'orders'
    ]

    @property
    @parse_date
    @first_element
    def last_updated_before(self):
        return self.xpath('./a:LastUpdatedBefore/text()')

    @property
    @first_element
    def _next_token(self):
        return self.xpath('./a:NextToken/text()')

    @property
    def next_token(self):
        n = self._next_token
        if n:
            return n.strip()
        return

    def orders(self):
        return [Order(x) for x in self.xpath('./a:Orders/a:Order')]

    def has_next(self):
        return bool(self.next_token)


class ListOrdersResponse(BaseElementWrapper):

    namespaces = {
        'a': 'https://mws.amazonservices.com/Orders/{}'.format(API_VERSION)
    }
    attrs = [
        'list_orders_result',
        'request_id'
    ]

    @property
    @first_element
    def _list_orders_result(self):
        return self.xpath('./a:ListOrdersResult|./a:ListOrdersByNextTokenResult')

    @property
    def list_orders_result(self):
        return ListOrdersResult(self._list_orders_result)

    @property
    @first_element
    def request_id(self):
        return self.xpath('./a:ResponseMetadata/a:RequestId/text()')
