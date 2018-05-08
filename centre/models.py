# -*- coding: utf-8 -*-
from django.db import models
from account.models import HeadUser
from common.models import Article

RISK_RANK = (
    ('1', '特危'),
    ('2', '高危'),
)


# Create your models here.
class RiskClosure(Article):
    author = models.ForeignKey(HeadUser, related_name='Article', on_delete=models.SET_NULL,
                               null=True, blank=True, verbose_name='作者')
    rank = models.CharField('风险等级', max_length=10, choices=RISK_RANK, default='2')

    class Meta:
        db_table = 'risk_closure'
        verbose_name = '风险提示'
        verbose_name_plural = verbose_name
