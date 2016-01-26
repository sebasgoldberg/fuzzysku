from django.contrib import admin
from default.models import Secao, Material, Familia, Sugestao
import autocomplete_light
from django.utils.functional import curry

class MaterialAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['cod_material', 'material', 'get_familias_sugeridas', 'familia']
    list_display_links = None
    list_editable = ['familia', ]
    search_fields = ['cod_material', 'material']
    list_filter = ['secao__secao', 'familia_sugerida', 'familia_selecionada']
    list_per_page = 40
    form = autocomplete_light.modelform_factory(Material, fields='__all__')

    def get_changelist_form(self, request, **kwargs):
        defaults = {
            "form": self.form,
            "formfield_callback": curry(self.formfield_for_dbfield,
                request=request),
            }
        defaults.update(kwargs)
        return autocomplete_light.modelform_factory(self.model, **defaults)

class FamiliaAdmin(admin.ModelAdmin):
    list_display_links = None
    actions = None
    list_display = ['cod_familia', 'familia', 'secao', 'cod_grupo', 'grupo', 'cod_subgrupo', 'subgrupo']
    search_fields = ['cod_familia', 'familia', 'secao__secao', 'grupo', 'subgrupo']
    list_filter = ['secao__secao', 'grupo',]
    list_per_page = 100

class SugestaoAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['material', 'selecionado', 'familia', 'score']
    list_display_links = None
    search_fields = ['material__cod_material', 'material__material']
    list_editable = ['selecionado', ]
    list_filter = [ 'material__secao__secao', 'material__familia_selecionada', 'material__multiplas_familias_selecionadas']
    list_per_page = 100

admin.site.register(Secao)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Familia, FamiliaAdmin)
admin.site.register(Sugestao, SugestaoAdmin)
