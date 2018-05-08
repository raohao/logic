# -*- coding: utf-8 -*-
from django.db import models
from account.models import HeadUser
from common.models import Receipt
from django.utils.timezone import now

# Create your models here.

SOLUTION = (
    ('1', '继续观察'),
    ('2', '提交阻断服务请求'),
    ('3', '其他处理方式'),
)


class AlarmCheck(Receipt):
    q_id = models.CharField('Qradar单号', max_length=32, null=True, blank=True)
    r_id = models.ForeignKey(HeadUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='受理人工号')
    re_id = models.CharField('Remedy单号', max_length=255, null=True, blank=True)
    classification = models.IntegerField('攻击类型', null=True, blank=True)
    s_ip = models.GenericIPAddressField('源IP', max_length=255, null=True, blank=True)
    d_ip = models.TextField('源目的IP', max_length=255, null=True, blank=True)
    s_address = models.CharField('源地址', max_length=255, null=True, blank=True)
    d_address = models.CharField('目的地址', max_length=255, null=True, blank=True)
    stream = models.IntegerField('流数目', null=True, blank=True)
    start_from = models.CharField('开始时间', max_length=255, null=True, blank=True)
    sustain = models.CharField('持续时间', max_length=255, null=True, blank=True)
    app = models.CharField('攻击应用', max_length=255, null=True, blank=True)
    solution = models.IntegerField('解决方式', choices=SOLUTION, default='1')

    class Meta:
        db_table = 'alarm_check'
        verbose_name = '监控告警单'
        verbose_name_plural = verbose_name


class EventCheck(Receipt):
    a_id = models.ForeignKey(AlarmCheck, on_delete=models.SET_NULL, related_name='a_id',
                             null=True, blank=True, verbose_name='关联告警单号')
    s_id = models.ForeignKey(HeadUser, on_delete=models.SET_NULL, related_name="s_id",
                             null=True, blank=True, verbose_name='建单人')
    r_id = models.ForeignKey(HeadUser, on_delete=models.SET_NULL, related_name='r_id',
                             null=True, blank=True, verbose_name='受理人')
    transmit = models.ForeignKey(HeadUser, on_delete=models.SET_NULL, related_name="transmit",
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
    id = models.CharField('单号', max_length=255, primary_key=True)
    time = models.DateTimeField('时间', auto_now_add=True, null=True, blank=True)
    judge = models.ManyToManyField(HeadUser, related_name="judge", verbose_name='评价人')
    candidate = models.ManyToManyField(HeadUser, related_name="candidate", verbose_name='被评人')
    score = models.IntegerField('分数', null=True, blank=True)
    reason = models.CharField('说明', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'evaluation'
        verbose_name = '员工评价单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class GuardPlan(models.Model):
    time = models.DateField('值班日期', primary_key=True, default=now)
    product_line = models.ForeignKey(HeadUser, related_name='product', on_delete=models.SET_NULL,
                                     null=True, blank=True, verbose_name='一线值班员')
    second_line = models.ForeignKey(HeadUser, related_name='second', on_delete=models.SET_NULL,
                                    null=True, blank=True, verbose_name='二线值班员')
    third_line = models.ForeignKey(HeadUser, related_name='third', on_delete=models.SET_NULL,
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
