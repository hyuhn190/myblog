# myblog/exceptions.py

import logging

logger = logging.getLogger(__name__)


class CacheException(Exception):
    pass

class DBException(Exception):
    pass

def catch_and_log(label=""):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"[UnknownException] {label}: {e}")
        return wrapper
    return decorator
