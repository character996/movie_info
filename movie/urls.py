from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'movie'
urlpatterns = [
    path('', TemplateView.as_view(template_name='movie/home.html'), name='home'),
    path('top250/', views.Top250View.as_view(), name='top250'),
    path('search/', views.search, name='search'),
    path('search_result/', views.SearchResultView.as_view(), name='search_result'),
    path('search/history/', views.HistoryView.as_view(), name='history'),
]
