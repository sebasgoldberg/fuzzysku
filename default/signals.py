#encoding=utf8
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from default.models import Sugestao, Material

def update_familia_selecionada(sender, instance, **kwargs):

    material = instance.material

    sugestoes_new = material.sugestao_set.all().count() > 0

    if material.familia_sugerida <> sugestoes_new:
        material.familia_sugerida = sugestoes_new
        material.save()

post_save.connect(update_familia_selecionada, 
    sender=Sugestao)
post_delete.connect(update_familia_selecionada, 
    sender=Sugestao)

def update_familia_material(sender, instance, **kwargs):

    familia_selecionada = (instance.familia is not None)

    if instance.familia_selecionada <> familia_selecionada:
        instance.familia_selecionada = familia_selecionada
        instance.save()
    
    instance.index()

post_save.connect(update_familia_material, 
    sender=Material)

