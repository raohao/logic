from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
import os


default_app_config = "guard.GuardConfig"


def autodiscover():
    autodiscover_modules('guard')


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class GuardConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = "值班工作"