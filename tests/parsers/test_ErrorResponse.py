import unittest

from mwstools.parsers.errors import ErrorResponse, _strip_namespace, ErrorElement, InvalidParameterValue


class ErrorResponseTests(unittest.TestCase):
    body = """
    <ErrorResponse xmlns="https://mws.amazonservices.com/Orders/2011-01-01">
      <Error>
        <Type>Sender</Type>
        <Code>InvalidParameterValue</Code>
        <Message>CreatedAfter or LastUpdatedAfter must be specified</Message>
      </Error>
      <RequestId>request-id</RequestId>
    </ErrorResponse>
    """

    def setUp(self):
        self.parser = ErrorResponse.load(self.body)

    def test_strip_namespace(self):
        self.assertEqual(_strip_namespace(self.body), """
    <ErrorResponse>
      <Error>
        <Type>Sender</Type>
        <Code>InvalidParameterValue</Code>
        <Message>CreatedAfter or LastUpdatedAfter must be specified</Message>
      </Error>
      <RequestId>request-id</RequestId>
    </ErrorResponse>
    """)

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'request-id')

    def test_raise_for_error(self):
        self.assertRaises(InvalidParameterValue, self.parser.raise_for_error)

    def test__error(self):
        self.assertIsNotNone(self.parser._error)

    def test_error(self):
        self.assertIsInstance(self.parser.error, ErrorElement)


__all__ = [
    ErrorResponseTests
]


def suite():
    s = unittest.TestSuite()
    for a in __all__:
        s.addTest(unittest.makeSuite(a))
    return s


if __name__ == '__main__':
    unittest.main(defaultTest='suite')

