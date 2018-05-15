# -*- coding: utf-8 -*-
from django.db import models
from common.models import (User, Profile, OrganizationInfo, DeptInfo, LogEntry)
from django.utils.translation import gettext_lazy as _
from common.validators import UnicodeUsernameValidator
from common.constant import (ADMIN_POWERLEVEL, HEAD_POWERLEVEL, BRANCH_POWERLEVEL)

# Create your models here.

'''
管理员用户相关数据库
'''


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

    @property
    def user_name(self):
        user_id = self.user_id
        user_profile = AdminUserProfile.objects.filter(id=user_id)
        if user_profile:
            return user_profile[0].name
        else:
            return '用户名不存在！'

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


'''
总行用户相关数据库
'''


class HeadUser(User):
    power_level = models.CharField('权限', max_length=64, choices=HEAD_POWERLEVEL, default='HeadAdmin')

    class Meta:
        db_table = 'head_user'
        verbose_name = '总行用户表'
        verbose_name_plural = verbose_name


class HeadOrganizationInfo(OrganizationInfo):
    organization_admin = models.ForeignKey(HeadUser, max_length=20, on_delete=models.SET_NULL,
                                           null=True, blank=True, verbose_name='管理员')

    @property
    def show_admin(self):
        user_id = self.organization_admin
        admin_info = HeadUserProfile.objects.filter(id=user_id)
        if admin_info:
            return admin_info[0].name + admin_info[0].tel + admin_info[0].email
        else:
            return '该部门未分配管理员！'

    class Meta:
        db_table = 'head_organization_info'
        verbose_name = '总行单位表'
        verbose_name_plural = verbose_name


class HeadUserProfile(Profile):
    user_id = models.OneToOneField(HeadUser, on_delete=models.CASCADE, verbose_name='用户')
    organization = models.ForeignKey(HeadOrganizationInfo, on_delete=models.CASCADE, verbose_name='单位')
    dept = models.CharField('团队代号', max_length=255, default='')
    remedy_user_id = models.CharField('remedy账号', max_length=64, default='')
    remedy_password = models.CharField('remedy密码', max_length=64, default='')

    class Meta:
        db_table = 'head_user_profile'
        verbose_name = '总行用户信息表'
        verbose_name_plural = verbose_name


class HeadDeptInfo(DeptInfo):
    organization = models.ForeignKey('HeadOrganizationInfo', max_length=255,
                                     on_delete=models.CASCADE, verbose_name='单位代号')

    class Meta:
        db_table = 'head_dept_info'
        unique_together = ('organization', 'dept',)
        verbose_name = '总行团队表'
        verbose_name_plural = verbose_name


'''
分行用户相关数据库
'''


class BranchUser(User):
    power_level = models.CharField(max_length=64, choices=BRANCH_POWERLEVEL, default='DeptOperator', verbose_name='权限')

    class Meta:
        db_table = 'branch_user'
        verbose_name = '分行用户表'
        verbose_name_plural = verbose_name


class BranchOrganizationInfo(OrganizationInfo):
    organization_admin = models.ForeignKey(BranchUser, max_length=20, on_delete=models.SET_NULL,
                                           null=True, blank=True, verbose_name='管理员')

    @property
    def show_admin(self):
        user_id = self.organization_admin
        admin_info = BranchUserProfile.objects.filter(id=user_id)
        if admin_info:
            return admin_info[0].name + admin_info[0].tel + admin_info[0].email
        else:
            return '该部门未分配管理员！'

    class Meta:
        db_table = 'branch_organization_info'
        verbose_name = '分行单位表'
        verbose_name_plural = verbose_name


class BranchUserProfile(Profile):
    user_id = models.OneToOneField(BranchUser, on_delete=models.CASCADE, verbose_name='用户')
    organization = models.ForeignKey(BranchOrganizationInfo, on_delete=models.CASCADE, verbose_name='单位代号')
    dept = models.CharField(max_length=255, verbose_name='部门代号', default='')

    class Meta:
        db_table = 'branch_user_profile'
        verbose_name = '分行用户信息表'
        verbose_name_plural = verbose_name


class BranchDeptInfo(DeptInfo):
    organization = models.ForeignKey('BranchOrganizationInfo', max_length=255,
                                     on_delete=models.CASCADE, verbose_name='单位代号')

    class Meta:
        db_table = 'branch_dept_info'
        unique_together = ('organization', 'dept',)
        verbose_name = '分行部门表'
        verbose_name_plural = verbose_name
