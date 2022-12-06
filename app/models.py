import ormar
import datetime


class DateTimeFieldsMixins:
    created_at: datetime = ormar.DateTime(default=datetime.datetime.utcnow())
    updated_at: datetime = ormar.DateTime(default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
