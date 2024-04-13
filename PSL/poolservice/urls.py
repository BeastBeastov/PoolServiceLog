from django.contrib import admin
from django.urls import path, re_path

from . import views
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('', main, name='begin'),
    path('home/', PoolServiceView.as_view(), name='home'),
    path('admin/', admin_view, name='admin'),
    path('about/', about, name='about'),
    path('new_log/', NewLogView.as_view(), name='new_log'),
    path('new_pool/', NewPoolView.as_view(), name='new_pool'),
    path('pool_show/<slug:pool_slug>/', PoolView.as_view(), name='pool_show'),
    path('pool_update/<slug:pool_slug>/', pool_update, name='pool_update'),
    path('pool_delete/<int:pk>/', DeletePoolView.as_view(), name='pool_delete'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    # path('register/', RegisterUser.as_view(), name='register'),
    # path('login/', LoginUser.as_view(), name='login'),
    # path('logout/', logout_user, name='logout'),
    path('log/<int:pk>/', LogView.as_view(), name='log'),
    path('update/<int:log_id>/', update_log, name='update'),
    path('delete/<int:pk>/', DeleteLogView.as_view(), name='delete'),
    path('pool_logs/<int:pool_id>/', PoolLogsView.as_view(), name='pool_logs'),
    path('add_reagent_name/', CreateReagentNameView.as_view(), name='add_reagent_name'),
    path('add_reagent_log/<int:pk>/', AddReagentView.as_view(), name='add_reagent_log'),
    path('delete_reagent_log/<int:pk>/', delete_reagent_log, name='delete_reagent_log'),
    path('export/<slug:pool_slug>/', export_to_excel, name='export_to_excel'),

]
