#encoding=utf8
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Min, Max

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

class Setor(models.Model):

    setor = models.CharField(max_length=100, verbose_name=_(u'Setor'), unique=True)

    def __unicode__(self):
        return u'%s' % self.setor

class BaseSecao(models.Model):
    
    cod_secao = models.CharField(max_length=2, verbose_name=_(u'Cod. Seção'), unique=True)
    secao = models.CharField(max_length=100, verbose_name=_(u'Seção'))

    class Meta:
        ordering = ['cod_secao']
        verbose_name = _(u"Seção")
        verbose_name_plural = _(u"Seções")
        app_label = 'default'
        abstract = True

    def __unicode__(self):
        return u'%s %s' % (self.cod_secao, self.secao)

    def acoes(self):
        return u"<a href='/default/dashboard_secao?cod_secao=%s' target='_blank'>%s</a>" % (
            self.cod_secao,_(u'Dashboard'))
    acoes.allow_tags = True
    acoes.short_description = _(u'Ações')


class Secao(BaseSecao):

    setor = models.ForeignKey(Setor, verbose_name=_(u'Setor'), null=True, blank=True)


class SecaoSAP(BaseSecao):
    secoes_destino_possiveis = models.ManyToManyField(Secao, verbose_name=_(u'Seções Novas Possiveis'))

    class Meta(BaseSecao.Meta):
        verbose_name = _(u"Seção SAP")
        verbose_name_plural = _(u"Seções SAP")
        app_label = 'default'

    def get_secoes_destino_possiveis(self):
        if self.secoes_destino_possiveis.exists():
            return u"<ul><li>%s</li></ul>" % u'</li><li>'.join([u'%s' % x for x in self.secoes_destino_possiveis.all()])
        return None
    get_secoes_destino_possiveis.allow_tags = True
    get_secoes_destino_possiveis.short_description = _(u'Seções Possiveis')
    

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
        return u'%s /%s/%s/%s/%s' % (self.cod_familia, self.secao.secao, self.grupo, self.subgrupo, self.familia)

    def completar_codigos(self):

        if self.cod_grupo == '' :
            familias = self.secao.familia_set.filter(grupo=self.grupo)
            if familias.exists():
                self.cod_grupo = familias.first().cod_grupo
            elif self.secao.familia_set.exists():
                min_cod_grupo = self.secao.familia_set.aggregate(Min('cod_grupo'))['cod_grupo__min']
                self.cod_grupo = str(int(min_cod_grupo) - 1)
            else:
                self.cod_grupo = self.secao.cod_secao + '99'
                if self.cod_subgrupo == '':
                    self.cod_subgrupo = self.cod_grupo + '01'
                if self.cod_familia == '':
                    self.cod_familia = self.cod_subgrupo + '001'
                return

        if self.cod_subgrupo == '':
            familias = self.secao.familia_set.filter(cod_grupo=self.cod_grupo, subgrupo=self.subgrupo)
            if familias.exists():
                self.cod_subgrupo = familias.first().cod_subgrupo
            elif self.secao.familia_set.filter(cod_grupo=self.cod_grupo).exists():
                max_cod_subgrupo = self.secao.familia_set.filter(cod_grupo=self.cod_grupo).aggregate(Max('cod_subgrupo'))['cod_subgrupo__max']
                self.cod_subgrupo = str(int(max_cod_subgrupo) + 1)
            else:
                self.cod_subgrupo = self.cod_grupo + '01'
                if self.cod_familia == '':
                    self.cod_familia = self.cod_subgrupo + '001'
                return

        if self.cod_familia == '':
            familias = self.secao.familia_set.filter(cod_grupo=self.cod_grupo, cod_subgrupo=self.cod_subgrupo, familia=self.familia)
            if familias.exists():
                self.cod_familia = familias.first().cod_familia
            elif self.secao.familia_set.filter(cod_grupo=self.cod_grupo, cod_subgrupo=self.cod_subgrupo).exists():
                max_cod_familia = self.secao.familia_set.filter(cod_grupo=self.cod_grupo, cod_subgrupo=self.cod_subgrupo).aggregate(Max('cod_familia'))['cod_familia__max']
                self.cod_familia = str(int(max_cod_familia) + 1)
            else:
                self.cod_familia = self.cod_subgrupo + '001'

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

    def es_delete(self):
        es = Elasticsearch()
        try:
            es.delete(index=ES_INDEX, doc_type=ES_DOC_TYPE, id=self.cod_familia)
        # @todo NotFoundError
        except:
            pass

    def tratar_sugeridos(self):
        if self.sugestao_set.exists():
            if self.sugestao_set.filter(material__familia_selecionada=False).exists():
                return u"<a href='/admin/default/sugestao/?q=%s' target='_blank'>%s</a>" % (
                    self.cod_familia,_(u'Tratar sugeridos'))
            return _(u'Sugeridos já tratados')
        return _(u'Sem açoes possivels')
    tratar_sugeridos.allow_tags = True
    tratar_sugeridos.short_description = _(u'Ações')

    def sugeridos_ja_tratados(self):
        if self.sugestao_set.filter(material__familia_selecionada=False).exists():
            return u'<img src="/static/admin/img/icon-no.svg" alt="False">'
        return u'<img src="/static/admin/img/icon-yes.svg" alt="True">'
    sugeridos_ja_tratados.allow_tags = True
    sugeridos_ja_tratados.short_description = _(u'Sugeridos já tratados')


class Material(models.Model):
    
    cod_material = models.CharField(max_length=20, verbose_name=_(u'Cod. Material'), unique=True)
    material = models.CharField(max_length=100, verbose_name=_(u'Material'))

    familia_sugerida = models.BooleanField(verbose_name=_(u'Familia Sugerida'), default=False)
    familia_selecionada = models.BooleanField(verbose_name=_(u'Familia Selecionada'), default=False)
    familia_em_sugeridas = models.BooleanField(verbose_name=_(u'Familia em Sugeridas'), default=False)
    relevante = models.BooleanField(verbose_name=_(u'Relevante'), default=False)

    secoes_possiveis = models.ManyToManyField(Secao, verbose_name=_(u'Seções Possiveis'), blank=True)
    familia = models.ForeignKey(Familia, verbose_name=_(u'Familia'), null=True, blank=True, on_delete=models.SET_NULL)
    secao_SAP = models.ForeignKey(SecaoSAP, verbose_name=_(u'Seção SAP'), null=True, blank=True, on_delete=models.SET_NULL)

    secao = models.ForeignKey(Secao, verbose_name=_(u'Nova Seção'), related_name='rel_secao', null=True, blank=True)

    class Meta:
        ordering = ['material']
        verbose_name = _(u"Material")
        verbose_name_plural = _(u"Materiais")
        app_label = 'default'

    def __unicode__(self):
        return u'%s %s' % (self.cod_material, self.material)

    def get_secoes_possiveis(self):
        return self.secoes_possiveis
    
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

        if self.secao is not None:
            cod_secao = [self.secao.cod_secao]
        else:
            cod_secao = [x.cod_secao for x in self.secoes_possiveis.all()]

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
                                'terms': { 'cod_secao': cod_secao, },
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

    def index_dict(self):

        setor = [ ]
        if self.familia is not None:
            if self.familia.secao.setor is not None:
                setor = [ self.familia.secao.setor.setor ]
            cod_secao = [ self.familia.secao.cod_secao ]
            secao = [ self.familia.secao.secao ]
        else:
            if self.secao is not None:
                if self.secao.setor is not None:
                    setor = [ self.secao.setor.setor ]
                cod_secao = [ self.secao.cod_secao ]
                secao = [ self.secao.secao ]
            else:
                cod_secao = [ ]
                secao = [ ]
                for x in self.secoes_possiveis.all():
                    if x.setor is not None:
                        setor.append(x.setor.setor)
                    cod_secao.append(x.cod_secao)
                    secao.append(x.secao)

        body = {
            "cod_material": self.cod_material,
            "material": self.material,
            "cod_secao": cod_secao,
            "secao": secao,
            "setor": setor,
            "familia_sugerida": self.familia_sugerida,
            "familia_selecionada": self.familia_selecionada,
            "familia_em_sugeridas": self.familia_em_sugeridas,
            "relevante": self.relevante,
            }
        if self.secao_SAP is not None:
            body["cod_secao_SAP"] = self.secao_SAP.cod_secao
            body["secao_SAP"] = self.secao_SAP.secao
        if self.familia is not None:
            body["cod_familia"] = self.familia.cod_familia
            body["familia"] = self.familia.familia
        return body
 
    def index_key(self):
        return self.cod_material

    def index(self):
        es = Elasticsearch()
        es.index(
            index=ES_FAMILIAS_INDEX,
            doc_type=ES_FAMILIAS_DOC_TYPE,
            id=self.index_key(),
            body=self.index_dict())

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

    def familia_aplicada(self):
        if self.material.familia_selecionada and self.familia.id == self.material.familia.id:
            value = u'checked'
            texto = _(u'Aplicada')
        else:
            value = u''
            texto = _(u'Não aplic.')
        return u'<input type="checkbox" class="familia-aplicada" id="check-%s" value="%s"><label for="check-%s">%s</label>' % (self.id, value, self.id, texto)
    familia_aplicada.allow_tags = True
    familia_aplicada.short_description = _(u'Familia aplicada')
