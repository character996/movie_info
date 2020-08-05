from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'movie_result'
urlpatterns = [
    path('', views.tags, name='home'),
    path('search_subjects/', cache_page(3*60)(views.search_subjects)),
    path('tags/', cache_page(3*60)(views.tags), name='tags'),
    path('type/', cache_page(3*60)(views.types), name='types'),
]
