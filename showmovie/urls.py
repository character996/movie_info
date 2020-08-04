"""showmovie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import settings
from movie_result import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('movie_result.urls')),
    path('', views.tags),
    path('user/', include('user.urls')),
    path('captcha/', include('captcha.urls')),
    path('api/', include('api.urls')),
    path('movie_result/', include('movie_result.urls')),
]

# 调试工具栏配置
if settings.DEBUG:

    import debug_toolbar

    urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))

