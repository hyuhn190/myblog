from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogView
from django.contrib.auth.decorators import login_required
from myblog.cache.clients import BlogCacheClient, BlogStatsService
from django.http import JsonResponse
from myblog.cache.cache_monitor import get_cache_stats
def blog_list(request):

    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog_list.html', {'blogs': blogs})


@login_required
def blog_detail(request, bid):
    u = request.user
    client = BlogCacheClient(bid)
    stats = BlogStatsService(bid, u.id)

    blog_data = client.get()
    stats.increase()

    total_views, uv_count, user_views = stats.get_stats()

    return render(request, 'blog_detail.html', {
        'blog': blog_data,
        'total_views': total_views,
        'unique_users': uv_count,
        'user_views': user_views,
    })



def cache_stats(request):
    stats = get_cache_stats()
    return JsonResponse(stats)