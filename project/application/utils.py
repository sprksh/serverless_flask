import shortuuid
from decimal import Decimal
from enum import Enum
import asyncio
import datetime
import logging
import time
import math
import functools

logger = logging.getLogger(__name__)


def get_short_uuid_of_length(length=6):
    return shortuuid.ShortUUID().random(length=length)


def make_jsonify_ready(obj):
    if isinstance(obj, list):
        response_list = list()
        for item in obj:
            response_list.append(make_jsonify_ready(item))
        return response_list
    if isinstance(obj, dict):
        response_dict = dict()
        for key, val in obj.items():
            response_dict[key] = make_jsonify_ready(val)
        return response_dict
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, Enum):
        return obj.value
    return obj


def timer(temp_logger=logger, log_level=logging.INFO):
    """
    Decorator to log timings
    """

    def decorator(func):
        @functools.wraps(func)
        def _timer(*args, **kwargs):
            ret = None
            st = time.time()
            start_time = math.ceil(st * (10 ** 5)) / (10 ** 2)
            ret = func(*args, **kwargs)
            et = time.time()
            response_time = math.ceil((et - st) * (10 ** 5)) / (10 ** 2)
            temp_logger.log(
                log_level, "-----------func %s time to execute: %s", func, response_time
            )
            return ret

        return _timer

    return decorator


def background(f):
    from functools import wraps

    @wraps(f)
    def wrapped(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        if callable(f):
            return loop.run_in_executor(None, f, *args, **kwargs)
        else:
            raise TypeError("Task must be a callable")

    return wrapped


def date_to_ymd_str(date_time):
    return date_time.strftime("%Y-%m-%d")


def ymd_str_to_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
