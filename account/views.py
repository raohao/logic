# -*- coding: utf-8 -*-
from django.views.decorators.cache import never_cache
from django.urls import path
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.contrib.auth import REDIRECT_FIELD_NAME
from account.forms import UserAuthenticationForm
from django.contrib.admin.forms import AdminAuthenticationForm
from functools import update_wrapper
from django.views.decorators.csrf import csrf_protect


class UserControl:

    login_title = '登陆页面'
    logout_template = 'logout.html'
    login_form = UserAuthenticationForm
    login_template = 'login.html'
    REDIRECT_FIELD_NAME = 'index'

    def __init__(self, name='user_control'):
        self.name = name

    def has_permission(self, request):
        """
        Return True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return request.user.is_active and request.user.is_staff

    def user_view(self, view, cacheable=False):
        def inner(request, *args, **kwargs):
            if not self.has_permission(request):
                if request.path == reverse('userauth:logout', current_app=self.name):
                    index_path = reverse('userauth:index', current_app=self.name)
                    return HttpResponseRedirect(index_path)
                # Inner import to prevent django.contrib.admin (app) from
                # importing django.contrib.auth.models.User (unrelated model).
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(
                    request.get_full_path(),
                    reverse('admin:login', current_app=self.name)
                )
            return view(request, *args, **kwargs)
        if not cacheable:
            inner = never_cache(inner)
        # We add csrf_protect here so this function can be used as a utility
        # function for any view, without having to repeat 'csrf_protect'.
        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)
        return update_wrapper(inner, view)

    @never_cache
    def login(self, request, extra_context=None):

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.user_view(view, cacheable)(*args, **kwargs)
            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        if request.method == 'GET' and self.has_permission(request):
            # Already logged-in, redirect to admin index
            index_path = reverse('common:home', current_app=self.name)
            return HttpResponseRedirect(index_path)

        from django.contrib.auth.views import LoginView
        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.admin.forms eventually imports User.
        context = dict(
            title=_('Log in'),
            app_path=request.get_full_path(),
            username=request.user.get_username(),
        )
        if (REDIRECT_FIELD_NAME not in request.GET and REDIRECT_FIELD_NAME not in request.POST):
            context[REDIRECT_FIELD_NAME] = reverse('common:home', current_app=self.name)
        context.update(extra_context or {})

        defaults = {
            'extra_context': context,
            'authentication_form': self.login_form,
            'template_name': self.login_template,
        }
        request.current_app = self.name
        return LoginView.as_view(**defaults)(request)

    # 注销操作函数
    @never_cache
    def logout(self, request, extra_context=None):
        from django.contrib.auth.views import LogoutView
        defaults = {
            'extra_context': dict(
                # Since the user isn't logged out at this point, the value of
                # has_permission must be overridden.
                has_permission=False,
                **(extra_context or {})
            ),
        }
        if self.logout_template is not None:
            defaults['template_name'] = self.logout_template
        request.current_app = self.name
        return LogoutView.as_view(**defaults)(request)

    # 类内URL路由
    def get_urls(self):
        urlpatterns = [
            path('login/', self.login, name='login'),
            path('logout/', self.logout, name='logout'),
        ]
        return urlpatterns

    # 类内URL路由入口
    @property
    def urls(self):
        return self.get_urls(), 'userauth', self.name

user_control = UserControl()
