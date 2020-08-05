from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'api'
urlpatterns = [
    path('movie/', views.get_movie, name='movie'),
    path('intro/', views.get_intro, name='intro'),
    path('tags/', cache_page(3*60)(views.tags)),
    path('type/', cache_page(3*60)(views.get_movie_for_type))
]
