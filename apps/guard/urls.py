# -*- coding: utf-8 -*-
from django.urls import path, include
from guard import views

app_name = 'guard'

urlpatterns = [
    path('', views.home, name='guard'),
    path('alarm', views.alarm.urls, name='alarm'),
]