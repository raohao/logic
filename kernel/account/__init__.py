# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
import os


default_app_config = "account.AccountConfig"


def autodiscover():
    autodiscover_modules('account')


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class AccountConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = "用户认证"