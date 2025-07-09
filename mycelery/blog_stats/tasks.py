# mycelery/blog_stats/tasks.py

from celery import shared_task
from django.core.cache import cache
from myblog.models import BlogView, Blog

@shared_task
def sync_blog_stats_to_db():
    for b in Blog.objects.all():
        uv_key = f"blog:{b.id}:views:userset"
        users = cache.smembers(uv_key) or []

        for u in users:
            try:
                u = int(u)
                cnt = cache.get(f"blog:{b.id}:views:user:{u}") or 0
                for _ in range(int(cnt)):
                    BlogView.objects.create(blog_id=b.id, user_id=u)
                cache.delete(f"blog:{b.id}:views:user:{u}")
            except Exception as e:
                print("[sync error]", e)

        cache.delete(f"blog:{b.id}:views:total")
        cache.delete(uv_key)

    print("同步完成")
