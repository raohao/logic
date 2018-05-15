# -*- coding: utf-8 -*-
from django.urls import path
from django.contrib.auth.decorators import login_required
from guard import views

app_name = 'guard'

urlpatterns = [
    path('', login_required(views.home), name='guard'),
    path('alarm', views.alarm.urls, name='alarm'),
]