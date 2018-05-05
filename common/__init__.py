from django.apps import AppConfig
import os

default_app_config = "common.CommonConfig"


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class CommonConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = "基本功能"