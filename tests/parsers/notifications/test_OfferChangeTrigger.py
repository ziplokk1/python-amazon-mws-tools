from unittest import TestCase
import datetime
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.notifications import OfferChangeTrigger


class TestOfferChangeTrigger(TestCase):

    body = """
    <OfferChangeTrigger>
        <MarketplaceId>marketplace-id</MarketplaceId>
        <ASIN>asin</ASIN>
        <ItemCondition>new</ItemCondition>
        <TimeOfOfferChange>2017-01-25T12:00:00.000Z</TimeOfOfferChange>
    </OfferChangeTrigger>
    """

    def setUp(self):
        self.parser = OfferChangeTrigger.load(self.body)

    def test_marketplace_id(self):
        self.assertEqual(self.parser.marketplace_id, 'marketplace-id')

    def test_asin(self):
        self.assertEqual(self.parser.asin, 'asin')

    def test_item_condition(self):
        self.assertEqual(self.parser.item_condition, 'new')

    def test_time_of_offer_change(self):
        self.assertEqual(self.parser.time_of_offer_change, datetime.datetime(2017, 1, 25, 6, 0, 0))

__all__ = [
    TestOfferChangeTrigger
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
