# myblog/cache/cache_monitor.py

import functools
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

CACHE_HIT_KEY = "cache:hit_count"
CACHE_MISS_KEY = "cache:miss_count"

def cache_monitor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        key = args[0].key if hasattr(args[0], 'key') else None

        if result is not None:
            try:
                cache.incr(CACHE_HIT_KEY)
            except:
                pass
        else:
            try:
                cache.incr(CACHE_MISS_KEY)
            except:
                pass
        return result
    return wrapper

def get_cache_stats():
    hit = int(cache.get(CACHE_HIT_KEY) or 0)
    miss = int(cache.get(CACHE_MISS_KEY) or 0)
    total = hit + miss
    rate = hit / total * 100 if total else 0
    return {"hit": hit, "miss": miss, "hit_rate": rate}
