from unittest import TestCase
from mwstools.parsers.products import GetLowestOfferListingsForAsinResponse


class TestGetLowestOfferListingsForAsinResponse(TestCase):

    body = """
    <GetLowestOfferListingsForASINResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <GetLowestOfferListingsForASINResult ASIN="asin" status="Success">
            <Empty />
        </GetLowestOfferListingsForASINResult>
        <ResponseMetadata>
            <RequestId>request-id</RequestId>
        </ResponseMetadata>
    </GetLowestOfferListingsForASINResponse>
    """

    def setUp(self):
        self.parser = GetLowestOfferListingsForAsinResponse.load(self.body)

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'request-id')

    def test_lowest_offer_listings(self):
        self.assertEqual(len(self.parser.lowest_offer_listings_result()), 1)
