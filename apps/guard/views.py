# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.urls import path
from django.views.decorators.cache import never_cache
from .models import AlarmCheck
from django.views.generic import ListView


def home(request):
    return render(request, 'actions.html')


class AlarmView:

    name = 'AlarmView'
    list_template = 'guard/AlarmCheckList.html'

    @never_cache
    def get_alarm_check_list(self, request, extra_context=None):
        from django.views.generic.list import ListView
        defaults = {
            'extra_context': dict(
                # Since the user isn't logged out at this point, the value of
                # has_permission must be overridden.
                has_permission=True,
                **(extra_context or {}),
            ),
            'queryset': AlarmCheck.objects.all(),
            'context_object_name': 'AlarmCheck',
            'paginate_by': 3,
        }
        if self.list_template is not None:
            defaults['template_name'] = self.list_template
        request.current_app = self.name
        return ListView.as_view(**defaults)(request)

    @never_cache
    def get_alarm_check(self, request, extra_context=None):
        from django.views.generic.list import ListView
        defaults = {
            'extra_context': dict(
                # Since the user isn't logged out at this point, the value of
                # has_permission must be overridden.
                has_permission=False,
                **(extra_context or {})
            ),
        }
        if self.list_template is not None:
            defaults['template_name'] = self.list_template
        request.current_app = self.name
        return ListView.as_view(**defaults)(request)

    def get_urls(self):
        urlpatterns = [
            path('', self.get_alarm_check_list, name='alarm_check_list'),
        ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'guard', self.name

    def get_check_list(self, request, *args, **kwargs):
        pass

alarm = AlarmView()
