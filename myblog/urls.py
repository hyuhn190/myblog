from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:bid>/', views.blog_detail, name='blog_detail'),
    path('stats/', views.cache_stats, name='cache_stats'),
]
