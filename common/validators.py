# -*- coding: utf-8 -*-
import re
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    regex = r'^[\w]+$'
    message = _(
        'Enter a valid username. This value may contain only English letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = re.ASCII


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w]+$'
    message = _(
        '请您使用英文字母自定义管理员用户名！'
    )
    flags = 0

@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^\d{7}$'
    message = _(
        '请使用您的工号注册！'
    )
    flags = 0