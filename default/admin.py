#encoding=utf8
from django.contrib import admin
from default.models import *
import autocomplete_light
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

admin.site.disable_action('delete_selected')

class MaterialAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['__unicode__', 'get_familias_sugeridas', 'familia']
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
    list_filter = ['secao__secao',]
    list_per_page = 100

class SugestaoAdmin(admin.ModelAdmin):

    def aplicar_familia(self, request, queryset):
        quan_familia_aplicada = 0
        quan_familia_ja_selecionada = 0
        for sugestao in queryset:
            try:
                sugestao.aplicar_familia()
                # @todo Actualizar Historial
                quan_familia_aplicada = quan_familia_aplicada + 1
            except FamiliaJaSelecionada:
                quan_familia_ja_selecionada = quan_familia_ja_selecionada + 1
        if quan_familia_aplicada > 0:
            self.message_user(request, _(u"%s materiais foram atualizados com sucesso.") % quan_familia_aplicada, level=messages.SUCCESS)
        if quan_familia_ja_selecionada > 0:
            self.message_user(request, _(u"%s materiais já tinham selecionada uma familia.") % quan_familia_ja_selecionada, level=messages.ERROR)
    aplicar_familia.short_description = _(u'Aplicar familia')

    actions = ['aplicar_familia', ]
    list_display = ['material', 'familia',]
    list_display_links = None
    search_fields = ['material__cod_material', 'material__material']
    list_filter = [ 'material__secao__secao', 'material__familia_selecionada', ]
    list_per_page = 100

admin.site.register(Secao)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Familia, FamiliaAdmin)
admin.site.register(Sugestao, SugestaoAdmin)
