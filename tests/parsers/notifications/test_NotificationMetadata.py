from unittest import TestCase

import datetime
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.notifications import NotificationMetadata


class TestNotificationMetadata(TestCase):

    body = """
    <NotificationMetaData>
        <NotificationType>AnyOfferChanged</NotificationType>
        <PayloadVersion>1.0</PayloadVersion>
        <UniqueId>unique-id</UniqueId>
        <PublishTime>2017-01-25T12:00:00.000Z</PublishTime>
        <SellerId>seller-id</SellerId>
        <MarketplaceId>marketplace-id</MarketplaceId>
    </NotificationMetaData>
    """

    def setUp(self):
        self.parser = NotificationMetadata.load(self.body)

    def test_notification_type(self):
        self.assertEqual(self.parser.notification_type, 'AnyOfferChanged')

    def test_payload_version(self):
        self.assertEqual(self.parser.payload_version, '1.0')

    def test_unique_id(self):
        self.assertEqual(self.parser.unique_id, 'unique-id')

    def test_publish_time(self):
        self.assertEqual(self.parser.publish_time, datetime.datetime(2017, 1, 25, 7, 0, 0))

    def test_seller_id(self):
        self.assertEqual(self.parser.seller_id, 'seller-id')

    def test_marketplace_id(self):
        self.assertEqual(self.parser.marketplace_id, 'marketplace-id')

__all__ = [
    TestNotificationMetadata
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
