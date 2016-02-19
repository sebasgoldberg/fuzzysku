#encoding=utf8
from django.contrib import admin
from default.models import *
import autocomplete_light
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

admin.site.disable_action('delete_selected')

class SugeridosJaTratadosListFilter(admin.SimpleListFilter):
    title = _(u'Sugeridos já tratados')
    parameter_name = 'sugeridos_ja_tratados'

    def lookups(self, request, model_admin):
        return (
            (0, _(u'Não')),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        familias_ids = [f.id for f in Familia.objects.raw( """
            select default_familia.id
            from default_familia
            where exists (
                select default_sugestao.id
                from default_sugestao inner join default_material
                on default_sugestao.material_id = default_material.id
                where
                    default_sugestao.familia_id = default_familia.id and
                    default_material.familia_selecionada = false
            )
            """)]
        return queryset.filter(id__in=familias_ids)

class SetorAdmin(admin.ModelAdmin):
    
    list_display_links = ['id']
    actions = None
    list_display = ['id', 'setor',]
    search_fields = ['setor', ]
    list_filter = []
    list_per_page = 40


class BaseSecaoAdmin(admin.ModelAdmin):
    list_display_links = ['id']
    actions = None
    list_display = ['id', 'cod_secao', 'secao', 'acoes']
    search_fields = ['cod_secao', 'secao', ]
    list_filter = []
    list_per_page = 40


class SecaoAdmin(BaseSecaoAdmin):
    list_display = ['id', 'cod_secao', 'secao', 'setor', 'acoes']
    #list_editable = [ 'setor', ]


class SecaoSAPAdmin(BaseSecaoAdmin):
    filter_horizontal = ['secoes_destino_possiveis']
    list_display = ['id', 'cod_secao', 'secao', 'get_secoes_destino_possiveis']


class MaterialAdmin(admin.ModelAdmin):

    def sugerir(self, request, queryset):

        quan_sugeridos = 0
        quan_nao_sugeridos = 0
        quan_selecao_realizada = 0

        for material in queryset:

            sugestoes = material.sugerir()
            material.salvar_sugestoes(sugestoes)
            
            if len(sugestoes) > 0:
                quan_sugeridos = quan_sugeridos + 1
            else:
                quan_nao_sugeridos = quan_nao_sugeridos + 1

        self.message_user(request, _(u'Materiais que tiverão sugestões: %s') %
            quan_sugeridos, level=messages.SUCCESS)
        self.message_user(request, _(u'Materiais que não tiverão sugestões: %s') %
            quan_nao_sugeridos, level=messages.WARNING)

    sugerir.short_description = _(u'Sugerir Familias')

    actions = ['sugerir', ]
 
    list_display = ['id', '__unicode__', 'get_familias_sugeridas', 'familia', 'secao', ]
    list_display_links = ['id']
    list_editable = ['familia', 'secao' ]
    search_fields = ['cod_material', 'material', 'familia__cod_familia']
    list_filter = ['familia_selecionada', 'familia_sugerida', 'secoes_possiveis__setor', 'secao__setor', 'secoes_possiveis', 'secao',]
    list_per_page = 40
    form = autocomplete_light.modelform_factory(Material, fields='__all__')
    filter_horizontal = ['secoes_possiveis', ]

    def get_changelist_form(self, request, **kwargs):
        defaults = {
            "form": self.form,
            "formfield_callback": curry(self.formfield_for_dbfield,
                request=request),
            }
        defaults.update(kwargs)
        return autocomplete_light.modelform_factory(self.model, **defaults)

class FamiliaAdmin(admin.ModelAdmin):
    list_display_links = ['id']
    actions = None
    list_display = ['id', 'sugeridos_ja_tratados', 'tratar_sugeridos', 'cod_familia', 'familia', 'secao', 'cod_grupo', 'grupo', 'cod_subgrupo', 'subgrupo', ]
    search_fields = ['cod_familia', 'familia', 'secao__secao', 'grupo', 'subgrupo']
    list_filter = [SugeridosJaTratadosListFilter, 'secao__setor', 'secao__secao', ]
    list_per_page = 40

class SugestaoAdmin(admin.ModelAdmin):

    def aplicar_familia(self, request, queryset):
        quan_familia_aplicada = 0
        quan_familia_ja_selecionada = 0
        for sugestao in queryset:
            try:
                sugestao.aplicar_familia()
                LogEntry.objects.log_action(
                    user_id = request.user.pk, 
                    content_type_id = ContentType.objects.get_for_model(sugestao.material).pk,
                    object_id = sugestao.material.pk,
                    object_repr = u'%s' % sugestao.material, 
                    action_flag = CHANGE,
                    change_message = _(u'Familia modificada massivamente')
                    )
                quan_familia_aplicada = quan_familia_aplicada + 1
            except FamiliaJaSelecionada:
                quan_familia_ja_selecionada = quan_familia_ja_selecionada + 1
        if quan_familia_aplicada > 0:
            self.message_user(request, _(u"%s materiais foram atualizados com sucesso.") % quan_familia_aplicada, level=messages.SUCCESS)
        if quan_familia_ja_selecionada > 0:
            self.message_user(request, _(u"%s materiais já tinham selecionada uma familia.") % quan_familia_ja_selecionada, level=messages.ERROR)
    aplicar_familia.short_description = _(u'Aplicar familia')

    actions = ['aplicar_familia', ]
    #list_display = ['id', 'familia_selecionada', 'familia_aplicada', 'material', 'familia']
    list_display = ['id', 'familia_selecionada', 'material', 'familia']
    list_display_links = ['id']
    search_fields = ['material__cod_material', 'material__material', 'familia__cod_familia', 'familia__familia']
    list_filter = [ 'material__familia_selecionada', 'familia__secao__setor', 'familia__secao', ]
    list_per_page = 40

admin.site.register(Setor, SetorAdmin)
admin.site.register(Secao, SecaoAdmin)
admin.site.register(SecaoSAP, SecaoSAPAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Familia, FamiliaAdmin)
admin.site.register(Sugestao, SugestaoAdmin)
