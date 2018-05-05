# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory
from django.http import HttpResponse
from guard import forms
from guard.models import AlarmCheck
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView
from django.views.decorators.cache import never_cache
from django.utils.timezone import now

def home(request, *args, **kwargs):
    return render(request, 'actions.html')


class AlarmView():

    name = 'AlarmView'

    def index(self, request):
        return render(request, 'base.html',)

    def get_urls(self):
        urlpatterns = [
            path('', self.index, name='index'),
        ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'guard', self.name

test = AlarmView()




decorators = [never_cache, login_required]


@method_decorator(decorators, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'invoice.html'


class AlarmCheckList(ListView):
    template_name = ''
    model = AlarmCheck
    context_object_name = 'alarmcheck_list'
    queryset = AlarmCheck.objects.order_by('s_time')


class AlarmCheckDetail(DetailView):
    model = AlarmCheck

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['alarmcheck_list'] = AlarmCheck.objects.all()
        return contex

    def get_object(self):
        object = super().get_object()
        object.id = now()
        object.save()


def apply_detail(request, check_id):
    '''
    显示一个工单详情
    :param request:
    :param order_id:   工单ID
    :return:
    '''
    if request.method == "GET":
        check_detail = AlarmCheck.objects.get(check_id=check_id)  # 取出这个条目的所有信息
        form = forms.ApplyUpdateForm(instance=check_detail)  # 把这个条目的信息塞入到表单里，instance就是从哪个对象里面获取数据
        render(request, 'form.html', {'selfforms': form})  # 把做好的表单返回到前端html文件里面通过form这个对象。

    elif request.method == "POST":  # 处理提交上来的数据
        form_obj = getattr(forms, "ApplyUpdateForm")# ApplyUpdateForm是在formself定义好的类
        fm_result = form_obj(request.POST)  # 把提交的数据塞入刚才的对象里面
        if fm_result.is_valid():   # 如果数据与数据库表之间能够匹配，也就是提交的表单内容正确
            fm_result.save()  # 那么就入库。
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('信息不全')


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AlarmCheck(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/admin/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AlarmCheck()

    return render(request, 'AlarmCheck.html', {'form': form})


def manage_alarm_check(request):
    alarm_check_set = modelformset_factory(AlarmCheck, fields=('name', 'title'))
    if request.method == 'POST':
        formset = alarm_check_set(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            # do something.
    else:
        formset = alarm_check_set()
    return render(request, 'AlarmCheck.html', {'formset': formset})


def query_alarm_check(request):
    alarm_check_set = modelformset_factory(AlarmCheck, fields=('name', 'title'))
    if request.method == "POST":
        formset = alarm_check_set(
            request.POST, request.FILES,
            queryset=AlarmCheck.objects.filter(name__startswith='O'),
        )
        if formset.is_valid():
            formset.save()
            # Do something.
    else:
        formset = alarm_check_set(queryset=AlarmCheck.objects.filter(name__startswith='O'))
    return render(request, 'AlarmCheck.html', {'formset': formset})