from django.contrib import admin
from default.models import Material, Familia, Sugestao

class MaterialAdmin(admin.ModelAdmin):
  list_display = ['cod_material', 'material', 'familia_selecionada']
  list_display_links = ('cod_material', 'material')
  search_fields = ['cod_material', 'material']
  list_filter = ['familia_selecionada']
  list_per_page = 100

class FamiliaAdmin(admin.ModelAdmin):
  list_display = ['id', 'cod_secao', 'secao', 'cod_grupo', 'grupo', 'cod_subgrupo', 'subgrupo', 'cod_familia', 'familia']
  list_display_links = [ 'id' ]
  search_fields = ['cod_familia', 'familia']
  list_filter = ['secao', 'grupo', 'subgrupo']
  list_per_page = 100

class SugestaoAdmin(admin.ModelAdmin):
  list_display = ['material', 'score', 'familia', 'selecionado']
  #list_display_links = ['id', ]
  search_fields = ['material__cod_material', 'material__material']
  list_editable = ['selecionado', ]
  list_filter = [ 'material__familia_selecionada', 'material__multiplas_familias_selecionadas']
  list_per_page = 100

# Register your models here.
admin.site.register(Material, MaterialAdmin)
admin.site.register(Familia, FamiliaAdmin)
admin.site.register(Sugestao, SugestaoAdmin)
