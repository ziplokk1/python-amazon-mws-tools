from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.products.get_my_fees_estimate import GetMyFeesEstimateResponse


class TestGetMyFeesEstimateResponse(TestCase):

    body = """
    <GetMyFeesEstimateResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <GetMyFeesEstimateResult>
            <FeesEstimateResultList>
                <FeesEstimateResult>
                    <Empty />
                </FeesEstimateResult>
                <FeesEstimateResult>
                    <Empty />
                </FeesEstimateResult>
                <FeesEstimateResult>
                    <Empty />
                </FeesEstimateResult>
                <FeesEstimateResult>
                    <Empty />
                </FeesEstimateResult>
            </FeesEstimateResultList>
        </GetMyFeesEstimateResult>
        <ResponseMetadata>
            <RequestId>request-id</RequestId>
        </ResponseMetadata>
    </GetMyFeesEstimateResponse>
    """

    def setUp(self):
        self.parser = GetMyFeesEstimateResponse.load(self.body)

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'request-id')

    def test_fees_estimate_result_list(self):
        self.assertEqual(len(self.parser.fees_estimate_result_list), 4)


__all__ = [
    TestGetMyFeesEstimateResponse
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')

