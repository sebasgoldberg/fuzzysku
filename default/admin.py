from django.contrib import admin
from default.models import Material, Familia, Sugestao

class MaterialAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['cod_material', 'material', 'familia_sugerida', 'familia_selecionada', 'multiplas_familias_selecionadas', 'familia']
    list_display_links = None
    list_editable = ['familia', ]
    search_fields = ['cod_material', 'material']
    list_filter = ['secao__secao', 'familia_sugerida', 'familia_selecionada', 'multiplas_familias_selecionadas']
    list_per_page = 100

class FamiliaAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['cod_familia', 'familia', 'secao', 'cod_grupo', 'grupo', 'cod_subgrupo', 'subgrupo']
    list_display_links = [ 'cod_familia' ]
    search_fields = ['cod_familia', 'familia']
    list_filter = ['secao__secao', 'grupo',]
    list_per_page = 100

class SugestaoAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['material', 'score', 'familia', 'selecionado']
    list_display_links = None
    search_fields = ['material__cod_material', 'material__material']
    list_editable = ['selecionado', ]
    list_filter = [ 'material__secao__secao', 'material__familia_selecionada', 'material__multiplas_familias_selecionadas']
    list_per_page = 100

# Register your models here.
admin.site.register(Material, MaterialAdmin)
admin.site.register(Familia, FamiliaAdmin)
admin.site.register(Sugestao, SugestaoAdmin)
