import re

from datetime import datetime
from pydantic import BaseModel, validator


class Request(BaseModel):
    cpu_usage: float
    device_id: str
    memory_usage: float
    timestamp: datetime

    class Config:
        orm_mode = True

    @validator('cpu_usage', 'memory_usage')
    def between_zero_and_one(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Value must be between 0 and 1')
        return v

    @validator('device_id')
    def less_than_100_chars(cls, v):
        if not len(v) < 100:
            raise ValueError('Value should contain less than 100 characters')
        return v

    @validator('timestamp', pre=True)
    def valid_timestamp(cls, v):
        # since this is a pre-validator, it expects a string value.
        # when returning a response from the DB, the type would be datetime.
        # skipping it since I can't be bothered improving the validator :)
        if isinstance(v, datetime):
            return v
        valid = re.compile('^[1-9]\d{3}-\d{2}-\d{2}[T\s]'
                           '\d{2}:\d{2}:\d{2}(\.\d{0,6})?(Z|\+00(:)?00)$')
        match = re.search(valid, v)
        if not match:
            raise ValueError('Value should be a valid RFC3339 UTC timestamp')
        return v
