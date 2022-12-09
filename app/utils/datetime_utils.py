import datetime


def datetime_to_timestamp(_datetime: datetime):
    return datetime.datetime.fromtimestamp(_datetime, tz=datetime.timezone.utc)


def get_millisecond_timestamp(_time: datetime):
    return round(_time.timestamp()*1000)
