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
from common.views import common_index
from account.views import user_control
from guard import urls as guard_urls
from centre import urls as centre_urls


urlpatterns = [
    path('', common_index.urls, name='index'),
    path('admin/', admin.site.urls),
    path('account/', user_control.urls, name='account'),
    path('guard/', include(guard_urls), name='guard'),
    path('centre/', include(centre_urls), name='centre')
]
