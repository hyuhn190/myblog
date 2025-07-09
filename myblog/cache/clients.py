# myblog/cache/clients.py

import json
from django.core.cache import cache
from myblog.models import Blog
from myblog.exceptions import CacheException
from myblog.cache.cache_monitor import cache_monitor

BLOG_CACHE_KEY = "blog:%s"
BLOG_CACHE_TTL = 3600

class BlogCacheClient:
    def __init__(self, bid):
        self.bid = bid
        self.key = BLOG_CACHE_KEY % bid

    @cache_monitor
    def get(self):
        data = cache.get(self.key)
        if data:
            return json.loads(data)

        b = Blog.objects.filter(id=self.bid).first()
        if not b:
            return None

        d = {
            'id': b.id,
            'title': b.title,
            'content': b.content,
            'author': b.author.username,
            'ctime': str(b.created_at),
        }

        try:
            cache.set(self.key, json.dumps(d), BLOG_CACHE_TTL)
        except Exception as e:
            pass  # 忽略缓存写入失败

        return d


STAT_KEY_TOTAL = "blog:%d:views:total"
STAT_KEY_USER = "blog:%d:views:user:%d"
STAT_KEY_UVISIT = "blog:%d:views:userset"

from django_redis import get_redis_connection

class BlogStatsService:
    def __init__(self, bid, uid):
        self.bid = bid
        self.uid = uid
        self.total_key = STAT_KEY_TOTAL % bid
        self.user_key = STAT_KEY_USER % (bid, uid)
        self.uv_key = STAT_KEY_UVISIT % bid
        self.r = get_redis_connection("default")

    def increase(self):
        r = self.r
        r.incr(self.total_key)
        r.incr(self.user_key)
        r.sadd(self.uv_key, self.uid)
        r.expire(self.total_key, 86400)
        r.expire(self.user_key, 86400)
        r.expire(self.uv_key, 86400)

    def get_stats(self):
        r = self.r
        t = r.get(self.total_key) or 0
        u = r.get(self.user_key) or 0
        uv = r.scard(self.uv_key) or 0
        return int(t), int(uv), int(u)
