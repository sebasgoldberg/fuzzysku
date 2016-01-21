#encoding=utf-8
from django.apps import AppConfig


class DefaultConfig(AppConfig):
    name = 'default'

    def ready(self, *args, **kwargs):
        
        from .signals import *
