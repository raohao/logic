# -*- coding: utf-8 -*-
from django.urls import path
from common import views

app_name = 'common'

urlpatterns = [
    path('common/', views.home, name='home'),
]