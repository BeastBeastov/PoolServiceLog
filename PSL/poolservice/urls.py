from django.contrib import admin
from django.urls import path, re_path

from . import views
from .views import *

urlpatterns = [
    path('', PoolServiceView.as_view(), name='home'),
    # path('admin/', admin, name='admin'),
    path('admin/', admin_view, name='admin'),
    path('about/', about, name='about'),
    path('development/', development, name='development'),
    path('new_log/', NewLogView.as_view(), name='new_log'),
    path('new_pool/', new_pool, name='new_pool'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('log/<int:log_id>/', show_log, name='log'),
    path('update/<int:log_id>/', update_log, name='update'),
    path('delete/<int:log_id>/', delete_log, name='delete'),
    path('pool_logs/<int:pool_id>/', PoolLogsView.as_view(), name='pool_logs'),
    path('pool_show/<slug:pool_slug>/', PoolView.as_view(), name='pool_show'),

    #path('pages/<slug:page>/', pages),
    #re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]
