from django.urls import path
from . import views

app_name = 'movie'
urlpatterns = [
    path('', views.home, name='home'),
    path('top250/', views.top250, name='top250'),
    path('search/', views.search, name='search'),
    # path('search_result/<title:int>', views.result, name='result'),
]
