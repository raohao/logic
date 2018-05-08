from django.contrib import admin
from guard.models import (AlarmCheck, EventCheck, Evaluation, GuardPlan)
# Register your models here.


@admin.register(AlarmCheck)
class AlarmCheckAdmin(admin.ModelAdmin):
    raw_id_fields = ('r_id',)
    list_per_page = 15

    class Meta:
        verbose_name = '监控告警单'
        verbose_name_plural = verbose_name


@admin.register(EventCheck)
class EventCheckAdmin(admin.ModelAdmin):
    raw_id_fields = ('a_id', 's_id', 'r_id')
    list_per_page = 5

    class Meta:
        verbose_name = '事件调查单'
        verbose_name_plural = verbose_name


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_per_page = 10

    class Meta:
        verbose_name = '考核评价单'
        verbose_name_plural = verbose_name


@admin.register(GuardPlan)
class GuardPlanAdmin(admin.ModelAdmin):
    raw_id_fields = ('product_line', 'second_line', 'third_line')
    list_per_page = 10

    class Meta:
        verbose_name = '值班安排表'
        verbose_name_plural = verbose_name
