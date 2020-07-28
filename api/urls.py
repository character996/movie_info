from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('movie/', views.AllMovieView.as_view(), name='movie'),
    path('intro/', views.get_intro, name='intro'),
]
