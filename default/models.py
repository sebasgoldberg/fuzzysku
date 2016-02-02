#encoding=utf8
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError

from elasticsearch import Elasticsearch

MAX_SUGESTOES = 5

ES_INDEX = "skuhier"
ES_DOC_TYPE = "skuhier"
ES_FAMILIAS_INDEX = 'familiasskus'
ES_FAMILIAS_DOC_TYPE = 'familiasskus'

if settings.TESTING:
    ES_INDEX = "test_%s" % ES_INDEX
    ES_FAMILIAS_INDEX = "test_%s" % ES_FAMILIAS_INDEX

class SecoesNaoCoincidem(ValidationError):
    pass

class CodigoSecaoNaoCoincide(ValidationError):
    pass

class CodigoGrupoNaoCoincide(ValidationError):
    pass

class CodigoSubGrupoNaoCoincide(ValidationError):
    pass

class FamiliaJaSelecionada(ValidationError):
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
        return u'%s %s' % (self.cod_secao, self.secao)

    def acoes(self):
        return u"<a href='/default/dashboard_secao?cod_secao=%s' target='_blank'>%s</a>" % (
            self.cod_secao,_(u'Dashboard'))
    acoes.allow_tags = True
    acoes.short_description = _(u'Ações')

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
        return u'%s /%s/%s/%s/%s' % (self.cod_familia, self.secao.secao, self.familia, self.grupo, self.subgrupo)

    def index(self):
        es = Elasticsearch()
        body = {
            "cod_secao": self.secao.cod_secao,
            "secao": self.secao.secao,
            "cod_grupo": self.cod_grupo,
            "grupo": self.grupo,
            "cod_subgrupo": self.cod_subgrupo,
            "subgrupo": self.subgrupo,
            "cod_familia": self.cod_familia,
            "familia": self.familia,
            }
        es.index(index=ES_INDEX, doc_type=ES_DOC_TYPE, id=self.cod_familia, body=body)

    def tratar_sugeridos(self):
        if self.sugestao_set.count() > 0:
            return u"<a href='/admin/default/sugestao/?q=%s' target='_blank'>%s</a>" % (
                self.cod_familia,_(u'Tratar sugeridos'))
        return _(u'Sem açoes possivels')
    tratar_sugeridos.allow_tags = True
    tratar_sugeridos.short_description = _(u'Ações')

class Material(models.Model):
    
    cod_material = models.CharField(max_length=20, verbose_name=_(u'Cod. Material'), unique=True)
    material = models.CharField(max_length=100, verbose_name=_(u'Material'))

    familia_sugerida = models.BooleanField(verbose_name=_(u'Familia Sugerida'), default=False)
    familia_selecionada = models.BooleanField(verbose_name=_(u'Familia Selecionada'), default=False)

    secao = models.ForeignKey(Secao, verbose_name=_(u'Seção'), related_name='rel_secao', null=True)
    secoes_possiveis = models.CharField(max_length=100, verbose_name=_(u'Seções Possiveis'), default='')
    familia = models.ForeignKey(Familia, verbose_name=_(u'Familia'), null=True, blank=True)

    #familias_sugeridas = models.ManyToManyField(Familia, verbose_name=_(u'Familias Sugeridas'), related_name='familias_sugeridas_set')

    class Meta:
        ordering = ['material']
        verbose_name = _(u"Material")
        verbose_name_plural = _(u"Materiais")
        app_label = 'default'

    def __unicode__(self):
        return u'%s %s' % (self.cod_material, self.material)

    def get_secoes_possiveis(self):
        cod_secoes = self.secoes_possiveis.split(' ')
        if len(cod_secoes) == 0 or self.secoes_possiveis == '':
            return [self.secao]
        return Secao.objects.filter(cod_secao__in=cod_secoes)
    
    @staticmethod
    def to_secoes_posiveis(secoes):
        return u' '.join( [ x.cod_secao for x in secoes ] )

    def get_familias_sugeridas(self):
        return '<ul>%s</ul>' % ''.join(
            [ '<li><a href="#" class="familia-sugerida">%s</a></li>' % x.familia for x in self.sugestao_set.all().order_by('-score') ])
    get_familias_sugeridas.short_description = _(u'Familias Sugeridas')
    get_familias_sugeridas.allow_tags = True

    def sugerir(self):

        es = Elasticsearch()
        body={
            'query': {
                'filtered':{
                    "query": {
                        "multi_match": {
                            "fields": ['secao', 'grupo', 'subgrupo', 'familia'],
                            "query": self.material,
                            "fuzziness": "AUTO",
                            }
                        },
                    'filter': {
                        'bool':{
                            'must':{
                                'terms': { 'cod_secao': self.secoes_possiveis.split(u' ') , },
                                }
                            }
                        }
                    }
                }
            }

        res = es.search(index=ES_INDEX, body=body)

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

        self.sugestao_set.all().delete()
        for (score, familia) in familias:
            self.sugestao_set.create(score=score, familia=familia)

    def index(self):
        es = Elasticsearch()
        if self.familia_selecionada:
            cod_secao = [ self.secao.cod_secao ]
            secao = [ self.secao.secao ]
        else:
            secoes_possiveis = self.get_secoes_possiveis()
            cod_secao = [ x.cod_secao for x in secoes_possiveis]
            secao = [ x.secao for x in secoes_possiveis]
        body = {
            "cod_material": self.cod_material,
            "material": self.material,
            "cod_secao": cod_secao,
            "secao": secao,
            "familia_sugerida": self.familia_sugerida,
            "familia_selecionada": self.familia_selecionada,
            }
        if self.familia is not None:
            body["cod_familia"] = self.familia.cod_familia
            body["familia"] = self.familia.familia
        es.index(index=ES_FAMILIAS_INDEX, doc_type=ES_FAMILIAS_DOC_TYPE, id=self.cod_material, body=body)

    def es_delete(self):
        es = Elasticsearch()
        try:
            es.delete(index=ES_FAMILIAS_INDEX, doc_type=ES_FAMILIAS_DOC_TYPE, id=self.cod_material)
        # @todo NotFoundError
        except:
            pass

class Sugestao(models.Model):
    
    material = models.ForeignKey(Material, verbose_name=_(u'Material'))
    familia = models.ForeignKey(Familia, verbose_name=_(u'Familia'))
    score = models.FloatField(verbose_name=_(u'Pontuação'), default=0)

    class Meta:
        ordering = ['familia', 'material',]
        verbose_name = _(u"Sugestão de Familias")
        verbose_name_plural = _(u"Sugestões de Familias")
        unique_together = (('familia', 'material', ),)
        app_label = 'default'

    def __unicode__(self):
        return _(u'Sugestão de %(familia)s para %(material)s') % {
            'material': self.material,
            'familia': self.familia,
            }

    def aplicar_familia(self):
        if self.material.familia is not None:
            raise FamiliaJaSelecionada(_(u'Familia %s já selecionada para material %s') % (self.familia, self.material))
        self.material.familia = self.familia
        self.material.save()
        self.material.refresh_from_db()

    def familia_selecionada(self):
        if self.material.familia_selecionada:
            return u'<img src="/static/admin/img/icon-yes.svg" alt="True">'
        return u'<img src="/static/admin/img/icon-no.svg" alt="False">'
    familia_selecionada.allow_tags = True
    familia_selecionada.short_description = _(u'Familia já selecionada')
