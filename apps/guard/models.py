# -*- coding: utf-8 -*-
from django.db import models
from account.models import HeadUser
from common.models import Receipt
from django.utils.timezone import now
from common.constant import (ALARM_CHECK_SOLUTION, GUARD_LEVEL)


# Create your models here.
class AlarmCheck(Receipt):
    qradar_id = models.CharField('Qradar单号', max_length=32, null=True, blank=True)
    receive_user_id = models.ForeignKey(HeadUser, on_delete=models.SET_NULL,
                                        null=True, blank=True, verbose_name='受理人工号')
    remedy_id = models.CharField('Remedy单号', max_length=255, null=True, blank=True)
    classification = models.IntegerField('攻击类型', null=True, blank=True)
    source_ip = models.GenericIPAddressField('源IP', max_length=255, null=True, blank=True)
    destination_ip = models.TextField('源目的IP', max_length=255, null=True, blank=True)
    source_address = models.CharField('源地址', max_length=255, null=True, blank=True)
    destination_address = models.CharField('目的地址', max_length=255, null=True, blank=True)
    stream = models.IntegerField('流数目', null=True, blank=True)
    start_from = models.CharField('开始时间', max_length=255, null=True, blank=True)
    sustain = models.CharField('持续时间', max_length=255, null=True, blank=True)
    app = models.CharField('攻击应用', max_length=255, null=True, blank=True)
    solution = models.IntegerField('解决方式', choices=ALARM_CHECK_SOLUTION, default='1')

    class Meta:
        db_table = 'alarm_check'
        verbose_name = '监控告警单'
        verbose_name_plural = verbose_name


class EventCheck(Receipt):
    alarm_check_id = models.ForeignKey(AlarmCheck, on_delete=models.SET_NULL, related_name='event_alarm_check',
                                       null=True, blank=True, verbose_name='关联告警单号')
    create_user_id = models.ForeignKey(HeadUser, on_delete=models.SET_NULL, related_name="event_create_user",
                                       null=True, blank=True, verbose_name='建单人')
    receive_user_id = models.ForeignKey(HeadUser, on_delete=models.SET_NULL, related_name='event_receive_user',
                                        null=True, blank=True, verbose_name='受理人')
    transmit_user_id = models.ForeignKey(HeadUser, on_delete=models.SET_NULL, related_name="event_transmit_user",
                                         null=True, blank=True, verbose_name='转派人')
    history = models.CharField('历史记录', max_length=255, null=True, blank=True)
    file = models.FileField('附件', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'event_check'
        verbose_name = '威胁事件单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 考核评价表
class Evaluation(models.Model):
    evaluation_id = models.CharField('单号', max_length=255, primary_key=True)
    create_time = models.DateTimeField('时间', auto_now_add=True, null=True, blank=True)
    judge_user_id = models.ForeignKey(HeadUser, related_name="evaluation_judge_user",
                                      on_delete=models.SET_NULL, null=True, blank=True, verbose_name='评价人')
    candidate_user_id = models.ForeignKey(HeadUser, related_name="evaluation_candidate_user",
                                          on_delete=models.SET_NULL, null=True, blank=True, verbose_name='被评人')
    score = models.IntegerField('分数', null=True, blank=True)
    reason = models.CharField('说明', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'evaluation'
        verbose_name = '员工评价单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class GuardPlan(models.Model):
    guard_plan_time = models.DateField('值班日期', primary_key=True, default=now)
    guard_level = models.CharField('保障等级', max_length=10, choices=GUARD_LEVEL, default='normal')
    product_user_id = models.ForeignKey(HeadUser, related_name='guard_product_user', on_delete=models.SET_NULL,
                                        null=True, blank=True, verbose_name='一线值班员')
    second_user_id = models.ForeignKey(HeadUser, related_name='guard_second_user', on_delete=models.SET_NULL,
                                       null=True, blank=True, verbose_name='二线值班员')
    third_user_id = models.ForeignKey(HeadUser, related_name='guard_third_user', on_delete=models.SET_NULL,
                                      null=True, blank=True, verbose_name='三线值班员')
    product_judge = models.FloatField('一线值班进度', default=0)
    second_judge = models.FloatField('二线值班进度', default=100)
    third_judge = models.FloatField('三线值班进度', default=100)
    report = models.FilePathField('日报', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'guard_plan'
        verbose_name = '值班安排表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id
