from unittest import TestSuite, main
from test_CompetitivePrice import suite as suite_competitive_price
from test_OfferListingCount import suite as suite_offer_listing_count
from test_Product import suite as suite_product
from test_SalesRank import suite as suite_sales_rank
from test_GetMatchingProductForIdProduct import suite as suite_get_matching_product_for_id_product
from test_GetMatchingProductForIdResponse import suite as suite_get_matching_product_for_id_response
from test_GetMatchingProductForIdResult import suite as suite_get_matching_product_for_id_result


def suite():
    s = TestSuite()
    s.addTest(suite_competitive_price())
    s.addTest(suite_offer_listing_count())
    s.addTest(suite_product())
    s.addTest(suite_sales_rank())
    s.addTest(suite_get_matching_product_for_id_product())
    s.addTest(suite_get_matching_product_for_id_response())
    s.addTest(suite_get_matching_product_for_id_result())
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
