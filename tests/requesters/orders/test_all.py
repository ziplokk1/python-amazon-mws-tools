from unittest import TestSuite, main
from test_ListOrdersRequester import suite as suite_list_orders_requester
from test_listOrderItemsRequester import suite as suite_list_order_items_requester


def suite():
    s = TestSuite()
    s.addTest(suite_list_orders_requester())
    s.addTest(suite_list_order_items_requester())
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
