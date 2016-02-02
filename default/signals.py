#encoding=utf8
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from default.models import *
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validar_material(sender, instance, **kwargs):
    secoes_possiveis = instance.get_secoes_possiveis()
    if instance.secao is None:
        instance.secao = secoes_possiveis[0]
    if instance.secoes_possiveis == '':
        instance.secoes_possiveis = instance.secao.cod_secao
    if instance.familia is None:
        return
    if instance.familia.secao not in secoes_possiveis:
        raise SecoesNaoCoincidem(_(u'A familia %s tem seção %s, mas o material %s pertece a seções %s') % (
            instance.familia,
            instance.familia.secao,
            instance,
            secoes_possiveis,
            ))
    instance.secao = instance.familia.secao

pre_save.connect(validar_material, 
    sender=Material)


def validar_familia(sender, instance, **kwargs):

    instance.cod_grupo = instance.cod_grupo.zfill(4)
    instance.cod_subgrupo = instance.cod_subgrupo.zfill(6)
    instance.cod_familia = instance.cod_familia.zfill(9)

    if instance.secao.cod_secao <> instance.cod_grupo[0:2]:
        raise CodigoSecaoNaoCoincide(_(u'Código de seção não coincide'))
    if instance.cod_grupo <> instance.cod_subgrupo[0:4]:
        raise CodigoGrupoNaoCoincide(_(u'Código de grupo não coincide'))
    if instance.cod_subgrupo <> instance.cod_familia[0:6]:
        raise CodigoSubGrupoNaoCoincide(_(u'Código de sub grupo não coincide'))

pre_save.connect(validar_familia, 
    sender=Familia)


def validar_secao(sender, instance, **kwargs):
    instance.cod_secao = instance.cod_secao.zfill(2)

pre_save.connect(validar_secao, 
    sender=Secao)


def update_familia_sugerida(sender, instance, **kwargs):

    material = instance.material

    sugestoes_new = material.sugestao_set.all().count() > 0

    if material.familia_sugerida <> sugestoes_new:
        material.familia_sugerida = sugestoes_new
        material.save()

post_save.connect(update_familia_sugerida, 
    sender=Sugestao)
post_delete.connect(update_familia_sugerida, 
    sender=Sugestao)


def update_familia_selecionada(sender, instance, **kwargs):

    familia_selecionada = (instance.familia is not None)

    if instance.familia_selecionada <> familia_selecionada:
        instance.familia_selecionada = familia_selecionada
        instance.save()

post_save.connect(update_familia_selecionada, 
    sender=Material)


def es_index_material(sender, instance, **kwargs):

    instance.index()

post_save.connect(es_index_material, 
    sender=Material)


def es_delete_material(sender, instance, **kwargs):
    instance.es_delete()

post_delete.connect(es_delete_material, 
    sender=Material)

    
def es_index_familia(sender, instance, **kwargs):

    instance.index()

post_save.connect(es_index_familia, 
    sender=Familia)


