# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from common.forms import EmailPostForm
from django.urls import path
from django.http import HttpResponse


# Create your views here.

class LogicEntry():

    def __init__(self, name='common'):
        self.name = name

    def index(self, response, *args, **kwargs):
        return HttpResponse('Hello!')

    # 类内URL路由
    def get_urls(self):
        urlpatterns = [
            path('', self.index, name='index'),
        ]
        return urlpatterns

    # 类内URL路由入口
    @property
    def urls(self):
        return self.get_urls(), 'common', self.name

common_index = LogicEntry()