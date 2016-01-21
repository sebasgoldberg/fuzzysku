from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from default.models import Sugestao

def update_familia_selecionada(sender, instance, **kwargs):

    material = instance.material

    quan_sugestoes = material.sugestao_set.all().count()

    sugestoes_new = False
    selecionado_new = False
    multiplas_new = False
    familia_new = None

    if quan_sugestoes <> 0:
        sugestoes_new = True
        quan_selecoes = material.sugestao_set.filter(selecionado=True).count()

        if quan_selecoes == 1:
            selecionado_new = True
            familia_new = material.sugestao_set.get(selecionado=True)
        elif quan_selecoes > 1:
            multiplas_new = True

    if ( material.familia_sugerida <> sugestoes_new or
        material.familia_selecionada <> selecionado_new or
        material.multiplas_familias_selecionadas <> multiplas_new or
        material.familia <> familia_new ):
        material.familia_sugerida = sugestoes_new
        material.familia_selecionada = selecionado_new
        material.multiplas_familias_selecionadas = multiplas_new
        material.familia = familia_new
        material.save()

post_save.connect(update_familia_selecionada, 
    sender=Sugestao)
post_delete.connect(update_familia_selecionada, 
    sender=Sugestao)
