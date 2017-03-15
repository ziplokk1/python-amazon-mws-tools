from unittest import TestSuite, main
from test_CompetitivePrice import suite as suite_competitive_price
from test_OfferListingCount import suite as suite_offer_listing_count
from test_Product import suite as suite_product
from test_SalesRank import suite as suite_sales_rank
from test_GetMatchingProductForIdProduct import suite as suite_get_matching_product_for_id_product
from test_GetMatchingProductForIdResponse import suite as suite_get_matching_product_for_id_response
from test_GetMatchingProductForIdResult import suite as suite_get_matching_product_for_id_result
from test_FeeDetail import suite as suite_fee_detail
from test_FeesEstimateResult import suite as suite_fees_estimate_result
from test_GetMyFeesEstimateResponse import suite as suite_get_my_fees_estimate_response
from get_my_price_for_sku import suite as suite_get_my_price_for_sku


def suite():
    s = TestSuite()
    s.addTest(suite_competitive_price())
    s.addTest(suite_offer_listing_count())
    s.addTest(suite_product())
    s.addTest(suite_sales_rank())
    s.addTest(suite_get_matching_product_for_id_product())
    s.addTest(suite_get_matching_product_for_id_response())
    s.addTest(suite_get_matching_product_for_id_result())
    s.addTest(suite_fee_detail())
    s.addTest(suite_fees_estimate_result())
    s.addTest(suite_get_my_fees_estimate_response())
    s.addTest(suite_get_my_price_for_sku())
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
