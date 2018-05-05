# -*- coding: utf-8 -*-
from django.urls import path
from userauth.views import UserLogin

app_name = 'userauth'

urlpatterns = [
    path('login', UserLogin.as_view(), name='login'),
]