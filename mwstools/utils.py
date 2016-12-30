import datetime
from dateutil import parser as DateParser


def _utc_offet():
    """
    Get the UTC offset for the current timezone.
    :return: The number of hours offset from UTC.
    """
    # Add 1 second to account for the time which it takes between calculating utcnow() and now()
    return int(((datetime.datetime.utcnow() - datetime.datetime.now()) + datetime.timedelta(
        seconds=1)).total_seconds() / 60 / 60)


def to_amazon_timestamp(dt):
    """
    Return string formatted datetime in amazon proper format with utc offset applied.

    :type dt: datetime.datetime
    :param dt:
    :return:
    """
    if not dt:
        return
    return (dt + datetime.timedelta(hours=_utc_offet())).strftime('%Y-%m-%dT%H:%M:%SZ')


def from_amazon_timestamp(ts):
    """
    Return a datetime object in local time.

    :param ts: Amazon string formatted timestamp.
    :return:
    """
    dt = DateParser.parse(ts).replace(tzinfo=None)
    return dt - datetime.timedelta(hours=_utc_offet())
