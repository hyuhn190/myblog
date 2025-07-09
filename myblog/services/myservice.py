# myblog/services/myservice.py

from myblog.cache.clients import BlogCacheClient, BlogStatsService
from myblog.models import BlogView
from django.contrib.auth.models import User

def get_blog_cache(blog_id):
    c = BlogCacheClient(blog_id)
    return c.get()

def record_blog(blog_id, user):
    s = BlogStatsService(blog_id, user.id)
    s.increase()
    BlogView.objects.create(blog_id=blog_id, user=user)

def get_blog_stats(blog_id, user):
    s = BlogStatsService(blog_id, user.id)
    return s.get_stats()
