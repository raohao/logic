# -*- coding: utf-8 -*-
"""logic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from account import urls as account_urls
from guard import urls as guard_urls
from common import urls as common_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(account_urls)),
    path('guard/', include(guard_urls)),
    path('common/', include(common_urls))
]
