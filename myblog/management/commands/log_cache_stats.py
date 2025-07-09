import logging
from django.core.management.base import BaseCommand
from myblog.cache.cache_monitor import get_cache_stats

logger = logging.getLogger('cache_stats_logger')

class Command(BaseCommand):
    help = '定时打印 Redis 缓存命中率'

    def handle(self, *args, **options):
        stats = get_cache_stats()
        logger.info(f"Redis缓存命中率统计: 命中={stats['hit']}, 未命中={stats['miss']}, 命中率={stats['hit_rate']:.2f}%")
