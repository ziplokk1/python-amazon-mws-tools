from unittest import TestSuite, main

from test_offer import suite as suite_offer
from test_getMyPriceForSkuResult import suite as suite_get_my_price_for_sku_result
from test_product import suite as suite_product
from test_getMyPriceForSkuResponse import suite as suite_get_my_price_for_sku_response

def suite():
    s = TestSuite()
    s.addTest(suite_offer())
    s.addTest(suite_get_my_price_for_sku_result())
    s.addTest(suite_product())
    s.addTest(suite_get_my_price_for_sku_response())
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
