"""
URL configuration for PSL project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.template.defaulttags import url
from django.urls import path, include, re_path

from django.views.generic.base import RedirectView
from django.templatetags.static import static
from django.conf.urls.static import static as static_urls

from django.conf import settings
from django.views.static import serve

from PSL import settings
from poolservice.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('users/', include('users.urls', namespace='users')),
    path('captcha/', include('captcha.urls')),
    path('', include('blog.urls')),
    path('', include('poolservice.urls')),
    path('api/v1/poolservicelist/', PoolServiceAPIView.as_view()),
    path("__debug__/", include("debug_toolbar.urls")),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
     urlpatterns += static_urls(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound # Обработчик будет работать только если в settings.py Debug = False

# admin.site.site_header = "Панель администрирования Эксперименты"
# admin.site.index_title = "Эксперименты Django"