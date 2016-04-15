#encoding=utf8
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed
from default.models import *
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

ELIMINAR_SECOES_EXISTENTES = False

def material_pre_save(sender, instance, **kwargs):

    familia_selecionada = (instance.familia is not None)

    if instance.familia_selecionada <> familia_selecionada:
        instance.familia_selecionada = familia_selecionada

    instance.familia_em_sugeridas = instance.sugestao_set.filter(
        familia=instance.familia).exists()

    instance.relevante = ( instance.secao_SAP is not None )

    if instance.pk is not None:
        if instance.secao_SAP is not None:
            if ELIMINAR_SECOES_EXISTENTES:
                instance.secao_SAP.secoes_destino_possiveis.delete()
            for secao in instance.secao_SAP.secoes_destino_possiveis.all():
                instance.secoes_possiveis.add(secao)

    if instance.familia is None:
        return

    if instance.secao is not None:
        if instance.secao.id <> instance.familia.secao.id:
            raise SecoesNaoCoincidem(_(u'A familia %s tem seção %s, mas o material %s pertece a seções %s') % (
                instance.familia,
                instance.familia.secao,
                instance,
                [instance.secao],
                ))

    elif not instance.secoes_possiveis.filter(pk=instance.familia.secao.pk).exists():
        raise SecoesNaoCoincidem(_(u'A familia %s tem seção %s, mas o material %s pertece a seções %s') % (
            instance.familia,
            instance.familia.secao,
            instance,
            list(instance.secoes_possiveis.all()),
            ))

pre_save.connect(material_pre_save, 
    sender=Material)


def secoes_possiveis_changed(sender, instance, action, **kwargs):
    if instance.secao is not None:
        return
    if not ( ( action == 'post_remove' ) or ( action == 'pre_remove' ) ):
        return
    if instance.familia is None:
        return
    if not instance.secoes_possiveis.filter(pk=instance.familia.secao.pk).exists():
        raise SecoesNaoCoincidem(_(u'A familia %s tem seção %s, mas o material %s pertece a seções %s') % (
            instance.familia,
            instance.familia.secao,
            instance,
            list(instance.secoes_possiveis.all()),
            ))

m2m_changed.connect(secoes_possiveis_changed,
    sender=Material.secoes_possiveis.through)


def validar_familia(sender, instance, **kwargs):
    
    instance.completar_codigos()

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

pre_save.connect(validar_secao, 
    sender=SecaoSAP)


def update_familia_sugerida(sender, instance, **kwargs):

    material = instance.material

    sugestoes_new = material.sugestao_set.all().count() > 0

    if material.familia_sugerida <> sugestoes_new:
        material.familia_sugerida = sugestoes_new
        material.save()

def sugestao_post_delete(sender, instance, **kwargs):
    update_familia_sugerida(sender, instance, **kwargs)
    if instance.material.familia == instance.familia:
        instance.material.familia_em_sugeridas = False
        instance.material.save()

post_save.connect(update_familia_sugerida, 
    sender=Sugestao)
post_delete.connect(sugestao_post_delete, 
    sender=Sugestao)


def update_material_post_save(sender, instance, created, **kwargs):

    save = False

    if created and instance.secao_SAP is not None:
        for secao in instance.secao_SAP.secoes_destino_possiveis.all():
            instance.secoes_possiveis.add(secao)
        save = True

    if save:
        instance.save()

    instance.index()

post_save.connect(update_material_post_save, 
    sender=Material)


def es_delete_material(sender, instance, **kwargs):
    instance.es_delete()

post_delete.connect(es_delete_material, 
    sender=Material)


def es_index_familia(sender, instance, **kwargs):

    instance.index()

post_save.connect(es_index_familia, 
    sender=Familia)


def es_delete_familia(sender, instance, **kwargs):

    instance.es_delete()

post_delete.connect(es_delete_familia, 
    sender=Familia)


