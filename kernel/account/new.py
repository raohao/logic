# -*- coding: utf-8 -*-
import account
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _, gettext_lazy
from django.views.decorators.cache import never_cache
from functools import update_wrapper
from django.views.decorators.csrf import csrf_protect



class UserAuth():
    site_url = '/'
    index_title = gettext_lazy('Site administration')
    _empty_value_display = '-'
    login_form = None
    index_template = None
    app_index_template = None
    login_template = None
    logout_template = None
    password_change_template = None
    password_change_done_template = None

    def __init__(self, name='UserAuth'):
        self.name = name

    def has_permission(self, request):
        return request.user.is_active

    def admin_view(self, view, cacheable=False):
        """
        Decorator to create an admin view attached to this ``AdminSite``. This
        wraps the view and provides permission checking by calling
        ``self.has_permission``.

        You'll want to use this from within ``AdminSite.get_urls()``:

            class MyAdminSite(AdminSite):

                def get_urls(self):
                    from django.urls import path

                    urls = super().get_urls()
                    urls += [
                        path('my_view/', self.admin_view(some_view))
                    ]
                    return urls

        By default, admin_views are marked non-cacheable using the
        ``never_cache`` decorator. If the view can be safely cached, set
        cacheable=True.

        """
        def inner(request, *args, **kwargs):
            if not self.has_permission(request):
                if request.path == reverse('admin:logout', current_app=self.name):
                    index_path = reverse('admin:index', current_app=self.name)
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

    def get_urls(self):
        from django.urls import include, path, re_path
        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.contenttypes.views imports ContentType.
        from django.contrib.contenttypes import views as contenttype_views

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        # Admin-site-wide views.
        urlpatterns = [
            path('', wrap(self.index), name='index'),
            path('login/', self.login, name='login'),
            path('logout/', wrap(self.logout), name='logout'),
            path('password_change/', wrap(self.password_change, cacheable=True), name='password_change'),
            path(
                'password_change/done/',
                wrap(self.password_change_done, cacheable=True),
                name='password_change_done',
            ),
            path(
                'r/<int:content_type_id>/<path:object_id>/',
                wrap(contenttype_views.shortcut),
                name='view_on_site',
            ),
        ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'admin', self.name

    def each_context(self, request):
        """
        Return a dictionary of variables to put in the template context for
        *every* page in the admin site.

        For sites running on a subpath, use the SCRIPT_NAME value if site_url
        hasn't been customized.
        """
        script_name = request.META['SCRIPT_NAME']
        site_url = script_name if self.site_url == '/' and script_name else self.site_url
        return {
            'site_url': site_url,
        }

    def password_change(self, request, extra_context=None):
        """
        Handle the "change password" task -- both form display and validation.
        """
        from account.forms import PasswordChangeForm
        from django.contrib.auth.views import PasswordChangeView
        url = reverse('userauth:password_change_done', current_app=self.name)
        defaults = {
            'form_class': PasswordChangeForm,
            'success_url': url,
            'extra_context': dict(self.each_context(request), **(extra_context or {})),
        }
        if self.password_change_template is not None:
            defaults['template_name'] = self.password_change_template
        request.current_app = self.name
        return PasswordChangeView.as_view(**defaults)(request)

    def password_change_done(self, request, extra_context=None):
        """
        Display the "success" page after a password change.
        """
        from django.contrib.auth.views import PasswordChangeDoneView
        defaults = {
            'extra_context': dict(self.each_context(request), **(extra_context or {})),
        }
        if self.password_change_done_template is not None:
            defaults['template_name'] = self.password_change_done_template
        request.current_app = self.name
        return PasswordChangeDoneView.as_view(**defaults)(request)

    @never_cache
    def logout(self, request, extra_context=None):
        """
        Log out the user for the given HttpRequest.

        This should *not* assume the user is already logged in.
        """
        from django.contrib.auth.views import LogoutView
        defaults = {
            'extra_context': dict(
                self.each_context(request),
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



    @never_cache
    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """

        context = dict(
            self.each_context(request),
            title=self.index_title,
        )

        request.current_app = self.name
        return TemplateResponse(request, 'index.html', context)

'''
def do_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_id = request.POST['user_id']
            password = request.POST['password']
            user = authenticate(request, user_id=user_id, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return render(request, 'index.html',)
            else:
                login_form.add_error(None, '用户名或密码错误！')
                return render(request, 'login.html')
        else:
            return render(request, 'error.html', )
    else:
        login_form =LoginForm()
        context = {}
        context['login_form'] = login_form

'''