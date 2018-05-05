# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views import View
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.template.response import TemplateResponse

class UserLogin(View):

    name = 'userauth'
    login_title = '登陆页面'

    @never_cache
    def get(self, request, *args, **kwargs):
#        login_path = reverse('userauth:login')
         return render(request, 'login.html')

    @never_cache
    def post(self, request, extra_context=None, *args, **kwargs):
        from django.contrib.auth.views import LoginView
        from userauth.forms import AuthenticationForm
        context = dict(
            username=request.user.get_username(),
            app_path=request.get_full_path(),
        )
        if (REDIRECT_FIELD_NAME not in request.GET and
                    REDIRECT_FIELD_NAME not in request.POST):
            context[REDIRECT_FIELD_NAME] = reverse('userauth:index')
        context.update(extra_context or {})

        defaults = {
            'extra_context': context,
            'authentication_form': AuthenticationForm,
            'template_name': 'login.html',
        }
        request.current_app = self.name
        return LoginView.as_view(**defaults)(request)

