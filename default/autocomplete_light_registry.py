#encoding=utf8

import autocomplete_light.shortcuts as al
from models import *

class FamiliaAutocomplete(al.AutocompleteModelBase):
    search_fields = ['secao__secao', 'grupo', 'subgrupo', 'familia', 'cod_familia']
    model = Familia

    def choices_for_request(self):
        material = Material.objects.get(cod_material = self.request.GET['cod_material'])
        if material.secao is not None:
            self.choices = self.choices.filter(secao=material.secao)
        else:
            self.choices = self.choices.filter(secao__in=material.secoes_possiveis.all())
        return super(FamiliaAutocomplete, self).choices_for_request()


class SecaoAutocomplete(al.AutocompleteModelBase):
    search_fields = ['secao__secao']
    model = Secao


al.register(FamiliaAutocomplete)
#al.register(SecaoAutocomplete)
