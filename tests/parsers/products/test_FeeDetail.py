from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.products.get_my_fees_estimate import FeeDetail


class TestFeeDetail(TestCase):

    body = """
    <FeeDetail xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <FeeAmount>
            <CurrencyCode>USD</CurrencyCode>
            <Amount>3.72</Amount>
        </FeeAmount>
        <FinalFee>
            <CurrencyCode>USD</CurrencyCode>
            <Amount>3.72</Amount>
        </FinalFee>
        <FeePromotion>
            <CurrencyCode>USD</CurrencyCode>
            <Amount>0.00</Amount>
        </FeePromotion>
        <FeeType>FBAFees</FeeType>
        <IncludedFeeDetailList>
            <FeeDetail>
                <FeeAmount>
                    <CurrencyCode>USD</CurrencyCode>
                    <Amount>1.66</Amount>
                </FeeAmount>
                <FinalFee>
                    <CurrencyCode>USD</CurrencyCode>
                    <Amount>1.66</Amount>
                </FinalFee>
                <FeePromotion>
                    <CurrencyCode>USD</CurrencyCode>
                    <Amount>0.00</Amount>
                </FeePromotion>
                <FeeType>FBAWeightHandling</FeeType>
            </FeeDetail>
            <FeeDetail>
                <FeeAmount>
                    <CurrencyCode>USD</CurrencyCode>
                    <Amount>1.06</Amount>
                </FeeAmount>
                <FinalFee>
                    <CurrencyCode>USD</CurrencyCode>
                    <Amount>1.06</Amount>
                </FinalFee>
                <FeePromotion>
                    <CurrencyCode>USD</CurrencyCode>
                    <Amount>0.00</Amount>
                </FeePromotion>
                <FeeType>FBAPickAndPack</FeeType>
            </FeeDetail>
            <FeeDetail>
                <FeeAmount>
                    <CurrencyCode>USD</CurrencyCode>
                    <Amount>1.00</Amount>
                </FeeAmount>
                <FinalFee>
                    <CurrencyCode>USD</CurrencyCode>
                    <Amount>1.00</Amount>
                </FinalFee>
                <FeePromotion>
                    <CurrencyCode>USD</CurrencyCode>
                    <Amount>0.00</Amount>
                </FeePromotion>
                <FeeType>FBAOrderHandling</FeeType>
            </FeeDetail>
        </IncludedFeeDetailList>
    </FeeDetail>
    """

    def setUp(self):
        self.parser = FeeDetail.load(self.body)

    def test_fee_amount(self):
        self.assertEqual(self.parser.fee_amount, '3.72')

    def test_final_fee(self):
        self.assertEqual(self.parser.final_fee, '3.72')

    def test_fee_promotion(self):
        self.assertEqual(self.parser.fee_promotion, '0.00')

    def test_fee_type(self):
        self.assertEqual(self.parser.fee_type, 'FBAFees')

    def test_included_fee_detail_list(self):
        self.assertEqual(len(self.parser.included_fee_detail_list), 3)

__all__ = [
    TestFeeDetail
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')


