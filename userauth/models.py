# -*- coding: utf-8 -*-
from django.db import models
from common.models import (User, LogEntry)
from django.utils.translation import gettext_lazy as _
from common.validators import UnicodeUsernameValidator

# Create your models here.

ADMIN_POWERLEVEL = (
    ('SysAdmin', '系统管理员'),
    ('HeadAdmin', '总行管理员'),
    ('BranchAdmin', '分行管理员'),
)

HEAD_POWERLEVEL = (
    ('TeanManager', '团队管理员'),
    ('GuardJudge', '值班审核员'),
    ('ClaimsMan', '事件调查员'),
    ('GuardManager', '值班管理员'),
    ('Temporary', '临时操作员'),
    ('Auditor', '审计检查员'),
)

BRANCH_POWERLEVEL = (
    ('BranchAssist', '分行协理员'),
    ('DeptManager', '部门管理员'),
    ('DeptOperator', '部门操作员'),
    ('Auditor', '审计检查员'),
)


class AdminUser(User):
    username_validator = UnicodeUsernameValidator()
    user_id = models.CharField(
        primary_key=True,
        max_length=20,
        help_text=_('请输入您的工号！'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        verbose_name='用户',
    )
    dept = models.CharField(max_length=255, verbose_name='团队', default='')
    power_level = models.CharField(max_length=64, choices=ADMIN_POWERLEVEL, default='3', verbose_name='权限')

    class Meta:
        db_table = 'AdminUser'
        verbose_name = '管理员用户表'
        verbose_name_plural = verbose_name


class HeadUser(User):
    dept = models.CharField(max_length=255, verbose_name='团队', default='')
    power_level = models.CharField(max_length=64, choices=HEAD_POWERLEVEL, verbose_name='权限', default='HeadAdmin')
    re_user_id = models.CharField(max_length=64, verbose_name='remedy账号', default='')
    re_password = models.CharField(max_length=64, verbose_name='remedy密码', default='')

    class Meta:
        db_table = 'HeadUser'
        verbose_name = '总行用户表'
        verbose_name_plural = verbose_name


class BranchUser(User):
    dept = models.CharField(max_length=255, verbose_name='部门', default='')
    power_level = models.CharField(max_length=64, choices=BRANCH_POWERLEVEL, default='DeptOperator', verbose_name='权限')

    class Meta:
        db_table = 'BranchUser'
        verbose_name = '分行用户表'
        verbose_name_plural = verbose_name


class DeptInfo(models.Model):
    organization = models.CharField(max_length=255)
    dept = models.CharField(max_length=255)
    organization_ch = models.CharField(max_length=255)
    dept_ch = models.CharField(max_length=255)
    mail = models.EmailField(max_length=64, null=True, blank=True)
    ceo = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'TeamInfo'
        unique_together = ('organization', 'dept',)

    def __str__(self):
        return str(self.organization_ch + ' ' + self.dept_ch)


