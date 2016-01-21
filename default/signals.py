from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from default.models import Sugestao

def update_familia_selecionada(sender, instance, **kwargs):

    material = instance.material

    try:
        material.sugestao_set.get(selecionado=True)
        selecionado_new = True
    except Sugestao.DoesNotExist:
        selecionado_new = False

    if material.familia_selecionada <> selecionado_new:
        material.familia_selecionada = selecionado_new
        material.save()

post_save.connect(update_familia_selecionada, 
    sender=Sugestao)
post_delete.connect(update_familia_selecionada, 
    sender=Sugestao)
