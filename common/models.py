# -*- coding: utf-8 -*-

#######################################################################################################################
# 文件作用：定义管理员、总行用户数据库模型
# 编写人：饶浩
# 修订日期：2018-4-22
#######################################################################################################################

from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission, Group)
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import (now, timedelta)

# Create your models here.
# 数据库除主键外大多数可空
# 常见问题：
# 1.数据库无法迁移：删除所有migration文件，清除数据库，重新生成文件；
# 2. ManytoManyField不能为空；
# 3.单张表多次引用其他表作为外键需要设置related_name；

INSTITUTION = (
    ('1', '总行'),
    ('2', '分行'),
)

ADMIN_POWERLEVEL = (
    ('1', '系统管理员'),
    ('2', '总行管理员'),
    ('3', '分行管理员'),
)

HEAD_POWERLEVEL = (
    ('1', '团队管理员'),
    ('2', '值班审核员'),
    ('3', '事件调查员'),
    ('4', '值班管理员'),
    ('5', '临时操作员'),
    ('6', '审计检查员'),
)

BRANCH_POWERLEVEL = (
    ('1', '分行协理员'),
    ('2', '部门管理员'),
    ('3', '部门操作员'),
    ('4', '合规管理员'),
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_id, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not user_id:
            raise ValueError('请设置用户名！')
        user_id = self.model.normalize_username(user_id)
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_id, password, **extra_fields)

    def create_superuser(self, user_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(user_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(primary_key=True, max_length=32, verbose_name='工号')
    name = models.CharField(max_length=20, verbose_name='姓名', default='')
    institution = models.CharField(max_length=64, verbose_name='机构', choices=INSTITUTION, default='1')
    organization = models.CharField(max_length=255, verbose_name='单位', db_index=True, default='')
    tel = models.CharField(max_length=255, verbose_name='电话', default='')
    email = models.EmailField(max_length=255, verbose_name='邮箱', default='')
    start_from = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    end_to = models.DateTimeField(default=(now().date() + timedelta(days=365)),verbose_name='有效期限')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    token = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['institution', ]

    def __str__(self):
        # __unicode__ on Python 2 return self.email @property def is_staff(self): 'Is the user a member of staff?'
        # Simplest possible answer: All admins are staff
        return str(self.is_admin)

    def get_full_name(self):
        return str(self.name)

    def get_short_name(self):
        return str(self.user_id)


    class Meta:
        ordering = ('institution', '-organization',)
        abstract = True


class AdminUser(User):
    dept = models.CharField(max_length=255, verbose_name='团队', default='')
    power_level = models.CharField(max_length=64, choices=ADMIN_POWERLEVEL, default='3', verbose_name='权限')
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('用户组'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='admin_user_set',
        related_query_name='admin_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('管理员用户权限'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='admin_user_set',
        related_query_name='admin_user',
    )

    class Meta:
        db_table = 'AdminUser'
        verbose_name = '管理员用户表'
        verbose_name_plural = verbose_name


class HeadUser(User):
    dept = models.CharField(max_length=255, verbose_name='团队', default='')
    power_level = models.CharField(max_length=64, choices=HEAD_POWERLEVEL, verbose_name='权限', default='5')
    re_user_id = models.CharField(max_length=64, verbose_name='remedy账号', default='')
    re_password = models.CharField(max_length=64, verbose_name='remedy密码', default='')
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('用户组'),
        blank=True,
        help_text=_(
            '请为用户组分配权限！'
        ),
        related_name='head_user_set',
        related_query_name='head_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('总行用户权限'),
        blank=True,
        help_text=_('请为用户分配权限！'),
        related_name='head_user_set',
        related_query_name='head_user',
    )

    class Meta:
        db_table = 'HeadUser'
        verbose_name = '总行用户表'
        verbose_name_plural = verbose_name


class BranchUser(User):
    dept = models.CharField(max_length=255, verbose_name='部门', default='')
    power_level = models.CharField(max_length=64, choices=BRANCH_POWERLEVEL, default='3', verbose_name='权限')
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('用户组'),
        blank=True,
        help_text=_(
            '请为用户组分配权限！'
        ),
        related_name='branch_user_set',
        related_query_name='branch_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('分行用户权限'),
        blank=True,
        help_text=_('请为用户分配权限！'),
        related_name='branch_user_set',
        related_query_name='branch_user',
    )

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


class Receipt(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    s_time = models.DateTimeField(auto_now_add=True, db_index=True )
    r_time = models.DateTimeField(null=True, blank=True)
    c_time = models.DateTimeField(null=True, blank=True)
    rank = models.CharField(max_length=10, null=True, blank=True)
    r_id = models.ForeignKey(HeadUser, on_delete=models.SET_NULL, null=True, blank=True)
    describe = models.TextField(max_length=3000, null=True, blank=True)
    influence = models.BooleanField(default=False)
    reason = models.TextField(max_length=3000, null=True, blank=True)
    solution = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.id