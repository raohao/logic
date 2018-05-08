# -*- coding: utf-8 -*-
from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('user_control/', views.user_control.urls, name='user'),
]