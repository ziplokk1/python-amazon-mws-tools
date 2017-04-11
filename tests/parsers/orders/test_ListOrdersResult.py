from unittest import TestCase, TestSuite, makeSuite, main
import datetime

from mwstools.parsers.orders import ListOrdersResult


class TestListOrdersResultFailed(TestCase):
    """
    Use case just to make sure that no errors are thrown when parsing non existent data.
    """

    body = """
    <ErrorResponse xmlns="https://mws.amazonservices.com/Orders/2013-09-01">
        <Error>
            <Type>Sender</Type>
            <Code>InvalidParameterValue</Code>
            <Message>CreatedAfter or LastUpdatedAfter must be specified</Message>
        </Error>
        <RequestId>request-id</RequestId>
    </ErrorResponse>
    """

    def setUp(self):
        self.parser = ListOrdersResult.load(self.body)

    def test_last_updated_before(self):
        self.assertIsNone(self.parser.last_updated_before)

    def test__next_token(self):
        self.assertIsNone(self.parser._next_token)

    def test_next_token(self):
        self.assertIsNone(self.parser.next_token)

    def test_orders(self):
        self.assertEqual(len(self.parser.orders()), 0)

    def test_has_next(self):
        self.assertFalse(self.parser.has_next())


class TestListOrdersResultNextTokenSuccess(TestCase):
    """
    The root element is different with a next token response. This tests to make sure that
    despite the root element being different, that the logic of the parser still properly functions.
    """

    body = """
    <ListOrdersByNextTokenResult xmlns="https://mws.amazonservices.com/Orders/2013-09-01">
        <Orders>
            <Order>
                <Empty />
            </Order>
        </Orders>
        <LastUpdatedBefore>2016-12-23T16:59:21Z</LastUpdatedBefore>
        <NextToken>next-token</NextToken>
    </ListOrdersByNextTokenResult>
    """

    def setUp(self):
        self.parser = ListOrdersResult.load(self.body)

    def test_last_updated_before(self):
        self.assertEqual(self.parser.last_updated_before, datetime.datetime(2016, 12, 23, 11, 59, 21))

    def test__next_token(self):
        self.assertIsNotNone(self.parser._next_token)

    def test_next_token(self):
        self.assertEqual(self.parser.next_token, 'next-token')

    def test_orders(self):
        self.assertEqual(len(self.parser.orders()), 1)

    def test_has_next(self):
        self.assertTrue(self.parser.has_next())


class TestListOrdersResultSuccess(TestCase):

    body = """
    <ListOrdersResult xmlns="https://mws.amazonservices.com/Orders/2013-09-01">
        <Orders>
            <Order>
                <Empty />
            </Order>
        </Orders>
        <LastUpdatedBefore>2016-12-22T17:37:50Z</LastUpdatedBefore>
        <NextToken>next-token</NextToken>
    </ListOrdersResult>
    """

    def setUp(self):
        self.parser = ListOrdersResult.load(self.body)

    def test_last_updated_before(self):
        self.assertEqual(self.parser.last_updated_before, datetime.datetime(2016, 12, 22, 12, 37, 50))

    def test__next_token(self):
        self.assertIsNotNone(self.parser._next_token)

    def test_next_token(self):
        self.assertEqual(self.parser.next_token, 'next-token')

    def test_orders(self):
        self.assertEqual(len(self.parser.orders()), 1)

    def test_has_next(self):
        self.assertTrue(self.parser.has_next())


__all__ = [
    TestListOrdersResultFailed,
    TestListOrdersResultNextTokenSuccess,
    TestListOrdersResultSuccess
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')

