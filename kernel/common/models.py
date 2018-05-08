# -*- coding: utf-8 -*-

#######################################################################################################################
# 文件作用：定义多种基础类型
# 编写人：饶浩
# 修订日期：2018-4-22
#######################################################################################################################
import json
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission, Group)
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import (now, timedelta)
from common.validators import UsernameValidator
from django.conf import settings
from common.utils import quote
from django.contrib.contenttypes.models import ContentType
from django.urls import NoReverseMatch, reverse
from django.utils import timezone
from django.utils.text import get_text_list
from django.utils.translation import gettext, gettext_lazy as _
from taggit.managers import TaggableManager

# Create your models here.
# 数据库除主键外大多数可空
# 常见问题：
# 1.数据库无法迁移：删除所有migration文件，清除数据库，重新生成文件；
# 2. ManytoManyField不能为空；
# 3.单张表多次引用其他表作为外键需要设置related_name；


def update_last_login(user,):
    """
    A signal receiver which updates the last_login date for
    the user logging in.
    """
    user.last_login = now()
    user.save(update_fields=['last_login'])


# 创建用户管理器
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

    INSTITUTION = (
        ('Head', '总行'),
        ('Branch', '分行'),
    )

    username_validator = UsernameValidator()
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
    institution = models.CharField('机构', max_length=64, choices=INSTITUTION, default='1')
    start_from = models.DateTimeField('创建时间', auto_now_add=True)
    end_to = models.DateTimeField('有效期限', default=(now().date() + timedelta(days=365)))
    power_level = models.CharField('权限', max_length=64, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['institution', ]
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('用户组权限'),
        blank=True,
        help_text=_(
            '请为用户组分配权限！'
        ),
        related_name='%(app_label)s_%(class)s_user_set',
        related_query_name='%(app_label)s_%(class)s_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('用户权限'),
        blank=True,
        help_text=_('请为用户分配权限！'),
        related_name='%(app_label)s_%(class)s_user_set',
        related_query_name='%(app_label)s_%(class)s_user',
    )

    def __str__(self):
        # __unicode__ on Python 2 return self.email @property def is_staff(self): 'Is the user a member of staff?'
        # Simplest possible answer: All admins are staff
        return str(self.is_admin)

    def get_full_name(self):
        return str(self.institution + self.user_id)

    def get_short_name(self):
        return str(self.user_id)

    class Meta:
        ordering = ('institution', '-organization',)
        abstract = True


class Profile(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    token = models.IntegerField('令牌', default=0)
    name = models.CharField('姓名', max_length=20, default='')
    photo = models.ImageField('头像')
    organization = models.CharField('单位', max_length=254, db_index=True, default='')
    tel = models.CharField('电话', max_length=254, default='')
    email = models.EmailField('邮箱', max_length=254, default='')

    class Meta:
        abstract = True


RECEIPT_STATUS = (
    ('new', '新建'),
    ('process', '处理中'),
    ('done', '完成'),
    ('close', '关闭'),
)

RECEIPT_RANK = (
    ('1', '一级安全事件'),
    ('2', '二级安全事件'),
    ('3', '三级安全事件'),
)


class Receipt(models.Model):
    check_id = models.CharField('单号', max_length=254, primary_key=True)
    title = models.CharField('标题', max_length=50, blank=True, default='')
    status = models.CharField('状态', max_length=10, choices=RECEIPT_STATUS, default='new')
    s_time = models.DateTimeField('发送时间', auto_now_add=True, db_index=True)
    r_time = models.DateTimeField('接收时间', null=True, blank=True)
    u_time = models.DateTimeField('更新时间', auto_now=True, null=True, blank=True)
    c_time = models.DateTimeField('关闭时间', null=True, blank=True)
    rank = models.CharField('等级', max_length=10, choices=RECEIPT_RANK, default='3')
    describe = models.TextField('描述', max_length=3000, null=True, blank=True)
    influence = models.BooleanField('影响', default=False)
    reason = models.TextField('原因', max_length=3000, null=True, blank=True)
    plan = models.TextField('解决方案', max_length=5000, null=True, blank=True)

    class Meta:
        ordering = ('s_time', )
        abstract = True

    def __str__(self):
        return self.check_id


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


ARTICLE_STATUS = (
    ('draft', '草稿'),
    ('published', '发布'),
)


class Article(models.Model):
    article_id = models.CharField('文章编号', max_length=50, primary_key=True)
    title = models.CharField('标题', max_length=250, default='', null=True, blank=True)
    slug = models.SlugField('简称', max_length=250, unique_for_date='publish', null=True, blank=True)
    author = models.CharField('作者', max_length=50, null=True, blank=True)
    body = models.TextField('正文', null=True, blank=True)
    s_time = models.DateTimeField('创建时间', auto_now_add=True)
    u_time = models.DateTimeField('修改时间', auto_now=True)
    p_time = models.DateTimeField('发布时间', default=now)
    status = models.CharField('状态', max_length=10, choices=ARTICLE_STATUS, default='draft')

    tags = TaggableManager()
    object = PublishedManager()

    class Meta:
        ordering = ('-publish',)
        abstract = True

    def __str__(self):
        return self.title


class Comments(models.Model):
    article_id = models.CharField('文章编号', max_length=50, null=True, blank=True)
    user_id = models.CharField('评论用户', max_length=15, null=True, blank=True)
    body = models.TextField('评论正文', max_length=500, default='', null=True, blank=True)
    s_time = models.DateTimeField('评论时间', auto_now_add=True)
    u_time = models.DateTimeField('更新时间', auto_now=True)
    active = models.BooleanField('用户状态', default=True)

    class Meta:
        ordering = ('s_time',)
        abstract = True

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user_id, self.article_id)


class LogEntryManager(models.Manager):
    use_in_migrations = True

    def log_action(self, user_id, content_type_id, object_id, object_repr, action_flag, change_message=''):
        if isinstance(change_message, list):
            change_message = json.dumps(change_message)
        return self.model.objects.create(
            user_id=user_id,
            content_type_id=content_type_id,
            object_id=str(object_id),
            object_repr=object_repr[:200],
            action_flag=action_flag,
            change_message=change_message,
        )


ADDITION = 1
CHANGE = 2
DELETION = 3


class LogEntry(models.Model):
    action_time = models.DateTimeField(
        _('action time'),
        default=timezone.now,
        editable=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_('user'),
    )
    content_type = models.ForeignKey(
        ContentType,
        models.SET_NULL,
        verbose_name=_('content type'),
        blank=True, null=True,
    )
    object_id = models.TextField(_('object id'), blank=True, null=True)
    # Translators: 'repr' means representation (https://docs.python.org/3/library/functions.html#repr)
    object_repr = models.CharField(_('object repr'), max_length=200)
    action_flag = models.PositiveSmallIntegerField(_('action flag'))
    # change_message is either a string or a JSON structure
    change_message = models.TextField(_('change message'), blank=True)

    objects = LogEntryManager()

    class Meta:
        db_table = '%(app_label)s_%(class)s_log'
        ordering = ('-action_time',)
        abstract = True

    def __repr__(self):
        return str(self.action_time)

    def __str__(self):
        if self.is_addition():
            return gettext('Added "%(object)s".') % {'object': self.object_repr}
        elif self.is_change():
            return gettext('Changed "%(object)s" - %(changes)s') % {
                'object': self.object_repr,
                'changes': self.get_change_message(),
            }
        elif self.is_deletion():
            return gettext('Deleted "%(object)s."') % {'object': self.object_repr}

        return gettext('LogEntry Object')

    def is_addition(self):
        return self.action_flag == ADDITION

    def is_change(self):
        return self.action_flag == CHANGE

    def is_deletion(self):
        return self.action_flag == DELETION

    def get_change_message(self):
        """
        If self.change_message is a JSON structure, interpret it as a change
        string, properly translated.
        """
        if self.change_message and self.change_message[0] == '[':
            try:
                change_message = json.loads(self.change_message)
            except ValueError:
                return self.change_message
            messages = []
            for sub_message in change_message:
                if 'added' in sub_message:
                    if sub_message['added']:
                        sub_message['added']['name'] = gettext(sub_message['added']['name'])
                        messages.append(gettext('Added {name} "{object}".').format(**sub_message['added']))
                    else:
                        messages.append(gettext('Added.'))

                elif 'changed' in sub_message:
                    sub_message['changed']['fields'] = get_text_list(
                        sub_message['changed']['fields'], gettext('and')
                    )
                    if 'name' in sub_message['changed']:
                        sub_message['changed']['name'] = gettext(sub_message['changed']['name'])
                        messages.append(gettext('Changed {fields} for {name} "{object}".').format(
                            **sub_message['changed']
                        ))
                    else:
                        messages.append(gettext('Changed {fields}.').format(**sub_message['changed']))

                elif 'deleted' in sub_message:
                    sub_message['deleted']['name'] = gettext(sub_message['deleted']['name'])
                    messages.append(gettext('Deleted {name} "{object}".').format(**sub_message['deleted']))

            change_message = ' '.join(msg[0].upper() + msg[1:] for msg in messages)
            return change_message or gettext('No fields changed.')
        else:
            return self.change_message

    def get_edited_object(self):
        """Return the edited object represented by this log entry."""
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def get_admin_url(self):
        """
        Return the admin URL to edit the object represented by this log entry.
        """
        if self.content_type and self.object_id:
            url_name = 'admin:%s_%s_change' % (self.content_type.app_label, self.content_type.model)
            try:
                return reverse(url_name, args=(quote(self.object_id),))
            except NoReverseMatch:
                pass
        return None
