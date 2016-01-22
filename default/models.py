#encoding=utf8
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from elasticsearch import Elasticsearch

MAX_SUGESTOES = 5

class SelecaoRealizadaException(Exception):
    pass

class Secao(models.Model):
    
    cod_secao = models.CharField(max_length=2, verbose_name=_(u'Cod. Seção'), unique=True)
    secao = models.CharField(max_length=100, verbose_name=_(u'Seção'))

    class Meta:
        ordering = ['cod_secao']
        verbose_name = _(u"Seção")
        verbose_name_plural = _(u"Seções")
        app_label = 'default'

    def __unicode__(self):
        return '%s %s' % (self.cod_secao, self.secao)


class Familia(models.Model):
    
    secao = models.ForeignKey(Secao, verbose_name=_(u'Seção'))
    cod_grupo = models.CharField(max_length=4, verbose_name=_(u'Cod. Grupo'))
    grupo = models.CharField(max_length=100, verbose_name=_(u'Grupo'))
    cod_subgrupo = models.CharField(max_length=6, verbose_name=_(u'Cod. Subgrupo'))
    subgrupo = models.CharField(max_length=100, verbose_name=_(u'Subgrupo'))
    cod_familia = models.CharField(max_length=9, verbose_name=_(u'Cod. Familia'), unique=True)
    familia = models.CharField(max_length=100, verbose_name=_(u'Familia'))

    class Meta:
        ordering = ['cod_familia']
        verbose_name = _(u"Familia")
        verbose_name_plural = _(u"Familias")
        app_label = 'default'

    def __unicode__(self):
        return '%s %s' % (self.cod_familia, self.familia)


class Material(models.Model):
    
    cod_material = models.CharField(max_length=20, verbose_name=_(u'Cod. Material'), unique=True)
    material = models.CharField(max_length=100, verbose_name=_(u'Material'))

    familia_sugerida = models.BooleanField(verbose_name=_(u'Familia sugerida'), default=False)
    familia_selecionada = models.BooleanField(verbose_name=_(u'Familia selecionada'), default=False)
    multiplas_familias_selecionadas = models.BooleanField(verbose_name=_(u'Multiplas Familias selecionadas'), default=False)

    secao = models.ForeignKey(Secao, verbose_name=_(u'Seção'), related_name='rel_secao')
    familia = models.ForeignKey(Familia, verbose_name=_(u'Familia'), null=True)

    class Meta:
        ordering = ['material']
        verbose_name = _(u"Material")
        verbose_name_plural = _(u"Materiais")
        app_label = 'default'

    def __unicode__(self):
        return '%s %s' % (self.cod_material, self.material)

    def sugerir(self):

        es = Elasticsearch()
        # @todo Modificar body para hacer una búsqueda fuzzy
        res = es.search(index="skuhier", body={
            "query": {
                "multi_match": {
                    "fields": ['secao', 'grupo', 'subgrupo', 'familia'],
                    "query": self.material,
                    "fuzziness": "AUTO",
                }
            }
        })

        result = []
        for hit in res['hits']['hits']:

            #source = hit["_source"]
            familia = Familia.objects.get(
                #cod_familia=source['cod_familia']
                cod_familia=hit['_id']
            )

            result.append( (hit['_score'], familia) )

            if len(result) >= MAX_SUGESTOES:
                break

        return result
    
    def salvar_sugestoes(self, familias):

        try:
            self.sugestao_set.get(selecionado=True)
            raise SelecaoRealizadaException()
        except Sugestao.DoesNotExist:
            pass

        self.familia_selecionada = False
        self.save()
        self.sugestao_set.all().delete()
        for (score, familia) in familias:
            self.sugestao_set.create(score=score, familia=familia)


class Sugestao(models.Model):
    
    material = models.ForeignKey(Material, verbose_name=_(u'Material'))
    familia = models.ForeignKey(Familia, verbose_name=_(u'Familia'))
    score = models.FloatField(verbose_name=_(u'Pontuação'), default=0)
    selecionado = models.BooleanField(verbose_name=_(u'Selecionado'), default=False)

    class Meta:
        ordering = ['material','-score']
        verbose_name = _(u"Sugestão de Familias")
        verbose_name_plural = _(u"Sugestões de Familias")
        unique_together = (('material', 'familia'),)
        app_label = 'default'

    def __unicode__(self):
        return _(u'Sugestão de %(familia)s para %(material)s') % {
            'material': self.material,
            'familia': self.familia,
            }

