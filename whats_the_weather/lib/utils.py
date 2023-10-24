"""Useful utils"""

from datetime import datetime, timedelta, timezone

from pydantic import validate_call

from .types import Timestamp, TimezoneOffset


@validate_call
def format_ts_tz_to_dt(timestamp: Timestamp, timezone_offset: TimezoneOffset):
    """Formats given timestamp to datetime object with given timezone_offset"""

    return datetime.fromtimestamp(timestamp, timezone.utc).astimezone(
        timezone(timedelta(seconds=timezone_offset))
    )
