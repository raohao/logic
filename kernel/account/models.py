# -*- coding: utf-8 -*-
from django.db import models
from common.models import (User, Profile,  LogEntry)
from django.utils.translation import gettext_lazy as _
from common.validators import UnicodeUsernameValidator


# Create your models here.
ADMIN_POWERLEVEL = (
    ('sys_admin', '系统管理员'),
    ('head_admin', '总行管理员'),
    ('branch_admin', '分行管理员'),
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

    power_level = models.CharField('权限', max_length=64, choices=ADMIN_POWERLEVEL, default='3')

    class Meta:
        db_table = 'admin_user'
        verbose_name = '管理员用户表'
        verbose_name_plural = verbose_name


class AdminUserProfile(Profile):
    user_id = models.OneToOneField(AdminUser, on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        db_table = 'admin_user_profile'
        verbose_name = '管理员用户信息表'
        verbose_name_plural = verbose_name

HEAD_POWERLEVEL = (
    ('team_manager', '团队管理员'),
    ('guard_judge', '值班审核员'),
    ('claims_man', '事件调查员'),
    ('guard_manager', '值班管理员'),
    ('temporary', '临时操作员'),
    ('auditor', '审计检查员'),
)


class HeadUser(User):
    power_level = models.CharField('权限', max_length=64, choices=HEAD_POWERLEVEL, default='HeadAdmin')

    class Meta:
        db_table = 'head_user'
        verbose_name = '总行用户表'
        verbose_name_plural = verbose_name


class HeadUserProfile(Profile):
    user_id = models.OneToOneField(HeadUser, on_delete=models.CASCADE, verbose_name='用户')
    dept = models.CharField('团队', max_length=255, default='')
    remedy_user_id = models.CharField('remedy账号', max_length=64, default='')
    remedy_password = models.CharField('remedy密码', max_length=64, default='')

    class Meta:
        db_table = 'head_user_profile'
        verbose_name = '总行用户信息表'
        verbose_name_plural = verbose_name


BRANCH_POWERLEVEL = (
    ('branch_assist', '分行协理员'),
    ('dept_manager', '部门管理员'),
    ('dept_operator', '部门操作员'),
    ('auditor', '审计检查员'),
)


class BranchUser(User):
    power_level = models.CharField(max_length=64, choices=BRANCH_POWERLEVEL, default='DeptOperator', verbose_name='权限')

    class Meta:
        db_table = 'branch_user'
        verbose_name = '分行用户表'
        verbose_name_plural = verbose_name


class BranchUserProfile(Profile):
    user_id = models.OneToOneField(BranchUser, on_delete=models.CASCADE, verbose_name='用户')
    dept = models.CharField(max_length=255, verbose_name='部门', default='')

    class Meta:
        db_table = 'branch_user_profile'
        verbose_name = '分行用户信息表'
        verbose_name_plural = verbose_name


class DeptInfo(models.Model):
    organization = models.CharField(max_length=255)
    dept = models.CharField(max_length=255)
    organization_ch = models.CharField(max_length=255)
    dept_ch = models.CharField(max_length=255)
    mail = models.EmailField(max_length=64, null=True, blank=True)
    ceo = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'team_info'
        unique_together = ('organization', 'dept',)
        verbose_name = '部门信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.organization_ch + ' ' + self.dept_ch)
