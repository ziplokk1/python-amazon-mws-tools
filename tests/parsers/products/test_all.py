from unittest import TestSuite, main
from test_CompetitivePrice import suite as suite_competitive_price
from test_OfferListingCount import suite as suite_offer_listing_count
from test_Product import suite as suite_product
from test_SalesRank import suite as suite_sales_rank


def suite():
    s = TestSuite()
    s.addTest(suite_competitive_price())
    s.addTest(suite_offer_listing_count())
    s.addTest(suite_product())
    s.addTest(suite_sales_rank())
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
