from unittest import TestCase
from unittest import TestSuite
from unittest import makeSuite
from unittest import main

from mwstools.parsers.notifications import AnyOfferChangedNotification


class TestAnyOfferChangedNotification(TestCase):

    body = """
    <AnyOfferChangedNotification>
        <OfferChangeTrigger>
            <Empty />
        </OfferChangeTrigger>
        <Summary>
            <Empty />
        </Summary>
        <Offers>
            <Offer>
                <Empty />
            </Offer>
            <Offer>
                <Empty />
            </Offer>
            <Offer>
                <Empty />
            </Offer>
        </Offers>
    </AnyOfferChangedNotification>
    """

    def setUp(self):
        self.parser = AnyOfferChangedNotification.load(self.body)

    def test_offer_change_trigger(self):
        self.assertIsNotNone(self.parser.offer_change_trigger)

    def test_summary(self):
        self.assertIsNotNone(self.parser.summary)

    def test_offers(self):
        self.assertEqual(len(self.parser.offers), 3)


class TestAnyOfferChangedNotificationNoOffers(TestCase):

    body = """
    <AnyOfferChangedNotification>
        <OfferChangeTrigger>
            <Empty />
        </OfferChangeTrigger>
        <Summary>
            <Empty />
        </Summary>
        <Offers />
    </AnyOfferChangedNotification>
    """

    def setUp(self):
        self.parser = AnyOfferChangedNotification.load(self.body)

    def test_offer_change_trigger(self):
        self.assertIsNotNone(self.parser.offer_change_trigger)

    def test_summary(self):
        self.assertIsNotNone(self.parser.summary)

    def test_offers(self):
        self.assertEqual(len(self.parser.offers), 0)


__all__ = [
    TestAnyOfferChangedNotification,
    TestAnyOfferChangedNotificationNoOffers
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')