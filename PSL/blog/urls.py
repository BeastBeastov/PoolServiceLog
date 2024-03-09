from django.contrib import admin
from django.urls import path, re_path

from . import views
from .views import *

urlpatterns = [
    #path('', BlogView.as_view(), name='blog'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('new_post/', CreatePostView.as_view(), name='new_post'),
    path('detail_post/<int:pk>/', DetailPostView.as_view(), name='detail_post'),
    path('delete_post/<int:pk>/', DeletePostView.as_view(), name='delete_post'),
    path('update_post/<int:pk>/', UpdatePostView.as_view(), name='update_post'),
    path('new_answer/<int:pk>/', new_answer, name='new_answer'),
]