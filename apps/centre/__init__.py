# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
import os


default_app_config = "centre.CentreConfig"


def autodiscover():
    autodiscover_modules('account')


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class CentreConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = "信息中心"