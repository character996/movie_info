from django.urls import path
from . import views

app_name = 'movie_result'
urlpatterns = [
    path('', views.tags, name='home'),
    path('search_subjects/', views.search_subjects),
    path('tags/', views.tags, name='tags'),
    path('type/', views.types, name='types'),
]
