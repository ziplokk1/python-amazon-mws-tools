from unittest import TestSuite, main
from test_AnyOfferChangedNotification import suite as any_offer_changed_notification_suite
from test_BuyBoxPrice import suite as buy_box_price_suite
from test_LowestPrice import suite as lowest_price_suite
from test_Notification import suite as notification_suite
from test_NotificationMetadata import suite as notification_metadata_suite
from test_Offer import suite as offer_suite
from test_OfferCount import suite as offer_count_suite


def suite():
    s = TestSuite()
    s.addTest(any_offer_changed_notification_suite())
    s.addTest(buy_box_price_suite())
    s.addTest(lowest_price_suite())
    s.addTest(notification_suite())
    s.addTest(notification_metadata_suite())
    s.addTest(offer_suite())
    s.addTest(offer_count_suite())
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
