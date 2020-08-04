from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('movie/', views.get_movie, name='movie'),
    path('intro/', views.get_intro, name='intro'),
    path('tags/', views.tags),
    path('type/', views.get_movie_for_type)
]
