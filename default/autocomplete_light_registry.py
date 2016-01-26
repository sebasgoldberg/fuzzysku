#encoding=utf8

import autocomplete_light.shortcuts as al
from models import Familia

# This will generate a PersonAutocomplete class.
al.register(
    Familia,
    # Just like in ModelAdmin.search_fields.
    search_fields=['secao__secao', 'grupo', 'subgrupo', 'familia'],
    attrs={
        # This will set the input placeholder attribute:
        'placeholder': 'Other model name ?',
        # This will set the yourlabs.Autocomplete.minimumCharacters
        # options, the naming conversion is handled by jQuery.
        'data-autocomplete-minimum-characters': 2,
        },
    # This will set the data-widget-maximum-values attribute on the
    # widget container element, and will be set to
    # yourlabs.Widget.maximumValues (jQuery handles the naming
    # conversion).
    widget_attrs={
        'data-widget-maximum-values': 10,
        # Enable modern-style widget !
        'class': 'modern-style',
        },
    )

