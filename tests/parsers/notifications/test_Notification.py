from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.notifications import Notification


class Dummy(object):
    """
    Only used for test_notification_payload since there is not actually a payload to test.
    """

    def __init__(self, *args, **kwargs):
        pass


class TestNotification(TestCase):

    body = """
    <Notification>
        <NotificationMetaData>
            <Empty />
        </NotificationMetaData>
        <NotificationPayload>
            <Emtpy />
        </NotificationPayload>
    </Notification>
    """

    def setUp(self):
        self.parser = Notification.load(self.body)

    def test_notification_metadata(self):
        self.assertIsNotNone(self.parser.notification_metadata)

    def test_notification_payload(self):
        self.assertIsNotNone(self.parser.notification_payload(Dummy))

__all__ = [
    TestNotification
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
