## Summary

This package is to be used in conjuction with [python-amazon-mws](https://github.com/czpython/python-amazon-mws).

The package contains simple wrappers for requesting orders and reports.

Not all API operations are supported yet.

## ToDo

* Create wrapper for products API
* Create descriptive documentation
* Add better comments to the modules

## Usage

## Requesters
* Any datetime parameters for requesters will automatically account for the UTC offset.
* * Ex. If you are in GMT-6 (Central Time) and pass datetime.datetime(2001, 1, 1) then the requester will convert that to "2001-01-01T06:00:00Z" for use with amazon's MWS API.

Catching exceptions:
```python
# All requesters will throw the same errors, so regardless of what requester
# you are using, the method remains the same.
from mwstools.requesters.reports import ReportRequester
from mwstools.parsers.errors import ErrorElement
from requests import HTTPError

report_requester = ReportRequester('access_key', 'secret_key', 'account_id', '_REPORT_TYPE_ENUMERATION_')
try:
    report_requester.request_and_download()
except ErrorElement as e:
    # Amazon sent back a response but the response body was an <ErrorResponse />
    print e
except HTTPError as e:
    print e
```

## Orders

List orders:
```python
import datetime

from requests import HTTPError
from mwstools.requesters.orders import ListOrdersRequester
from mwstools.parsers.errors import ErrorElement

requester = ListOrdersRequester('access_key', 'secret_key', 'account_id')
try:
    # any datetime objects passed to the orders 
    list_orders_parser = requester.request(last_updated_after=datetime.datetime.now())
except HTTPError:
    raise
except ErrorElement:
    # Missing parameter, invalid date, etc. (Anything that amazon replies with a 200 status code but an ErrorResponse element)
    raise
    
for order in list_orders_parser.list_orders_result.orders():
    print order.amazon_order_id, order.buyer_name
```

List order items:
```python
from requests import HTTPError
from mwstools.requesters.orders import ListOrderItemsRequester
from mwstools.parsers.errors import ErrorElement

requester = ListOrderItemsRequester('access_key', 'secret_key', 'account_id')
try:
    list_order_items_parser = requester.request('xxx-xxxxxxx-xxxxxxx')
except HTTPError:
    raise
except ErrorElement:
    # If you run this exact snippet of code, ErrorElement will be raised and the message will be something along the lines of "InvalidParameterValue: Invalid order id for xxx-xxxxxxx-xxxxxxx".
    # Whatever the message is in the <Message> element of the <Error>.
    raise

for order_item in list_order_items_parser.order_items():
    print order_item.order_item_id, order_item.seller_sku, order_item.amazon_order_id
```

### Reports

Requesting and downloading a new report:
```python
from mwstools.requesters.reports import ReportRequester

report_requester = ReportRequester('access_key', 'secret_key', 'account_id', '_REPORT_TYPE_ENUMERATION_')
report_contents = report_requester.request_and_download()
print report_contents
```

Requesting a new report:
```python
from mwstools.requesters.reports import ReportRequester
report_requester = ReportRequester('access_key', 'secret_key', 'account_id', '_REPORT_TYPE_ENUMERATION_')
requested_report_response = report_requester.request()
report_request_id = requested_report_response.request_report_result.report_request_id
print report_request_id
```

Waiting for a report to download:
```python
from mwstools.requesters.reports import ReportRequester
report_requester = ReportRequester('access_key', 'secret_key', 'account_id', '_REPORT_TYPE_ENUMERATION_')
report_request_id = 'test-id'
generated_report_id = report_requester.poll(report_request_id)
print generated_report_id
```

Downloading a report by generated report id:
```python
from mwstools.requesters.reports import ReportRequester
report_requester = ReportRequester('access_key', 'secret_key', 'account_id', '_REPORT_TYPE_ENUMERATION_')
generated_report_id = 'test-id'
report_contents = report_requester.download(generated_report_id)
print report_contents
```