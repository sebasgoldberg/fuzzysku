#encoding=utf-8
from django.apps import AppConfig


class DefaultConfig(AppConfig):
    name = 'default'

    def ready(self, *args, **kwargs):
        
        from .signals import *

        """
        import autocomplete_light.shortcuts as autocomplete_light

        class DefaultConfigAutocomplete(autocomplete_light.AutocompleteListBase):
            choices = ['a', 'b']

        autocomplete_light.register(DefaultConfigAutocomplete)
        """
        from autocomplete_light_registry import *
