# -*- coding: utf-8 -*-

from django import forms
from .models import (AlarmCheck, EventCheck)


class AlarmCheckForm(forms.ModelForm):
    class Meta:
        model = AlarmCheck
        fields = '__all__'


class EventCheckForm(forms.ModelForm):
    class Meta:
        model = EventCheck
        fields = '__all__'


class CreatAlarmCheckForm(forms.ModelForm):
    class Meta:
        model = AlarmCheck
        fields = '__all__'


class ChangeAlarmCheckForm(forms.ModelForm):
    class Meta:
        model = AlarmCheck
        fields = '__all__'


class ApplyUpdateForm(forms.ModelForm):
    class Meta:
        model = AlarmCheck    # 和哪个数据库绑定在一块
        fields = '__all__'
        exclude = ()   # 排除哪个字段

    def __init__(self, *args, **kwargs):
        #  继承父类，后重写自己的类
        super(ApplyUpdateForm, self).__init__(*args, **kwargs)

        for field_name in self.base_fields:   # 遍历每一个字段
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})  # 给每一个输入框添加上一个样式