#encoding=utf8

import autocomplete_light.shortcuts as al
from models import Familia, Material

class FamiliaAutocomplete(al.AutocompleteModelBase):
    search_fields = ['secao__secao', 'grupo', 'subgrupo', 'familia', 'cod_familia']
    model = Familia

    def choices_for_request(self):
        material = Material.objects.get(cod_material = self.request.GET['cod_material'])
        self.choices = self.choices.filter(secao__id=material.secao.id)
        return super(FamiliaAutocomplete, self).choices_for_request()

al.register(FamiliaAutocomplete)
