# -*- coding: utf-8 -*-
from django.db import models
from common.models import LogEntry
from account.models import (HeadUser, BranchUser)
from django.utils.translation import gettext_lazy as _

# Create your models here.


class AdminLogEntry(LogEntry):
    class Meta:
        verbose_name = '管理员操作日志'
        verbose_name_plural = verbose_name


class HeadLogEntry(LogEntry):
    user = models.ForeignKey(
        HeadUser,
        models.CASCADE,
        verbose_name=_('user'),
    )

    class Meta:
        verbose_name = '总行员工操作日志'
        verbose_name_plural = verbose_name


class BranchLogEntry(LogEntry):
    user = models.ForeignKey(
        BranchUser,
        models.CASCADE,
        verbose_name=_('user'),
    )

    class Meta:
        verbose_name = '分员工操作日志'
        verbose_name_plural = verbose_name
