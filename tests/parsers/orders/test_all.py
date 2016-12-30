from unittest import TestSuite, main
from test_Order import suite as suite_order
from test_OrderItem import suite as suite_order_item
from test_ListOrderItemsResponse import suite as suite_list_order_items_response
from test_ListOrdersResult import suite as suite_list_orders_result
from test_ListOrdersResponse import suite as suite_list_orders_response


def suite():
    s = TestSuite()
    s.addTest(suite_order())
    s.addTest(suite_order_item())
    s.addTest(suite_list_order_items_response())
    s.addTest(suite_list_orders_result())
    s.addTest(suite_list_orders_response())
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
