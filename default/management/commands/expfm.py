#encoding=utf8
from django.core.management.base import BaseCommand, CommandError
from default.models import *
from multiprocessing import Pool
from els.utils import ElasticFilesGenerator
import sys
import codecs
from django.db.models import Q
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

class Command(BaseCommand):
    help = 'Gera um arquivo de familias separado por tabuladores.'

    def add_arguments(self, parser):
        parser.add_argument('cod_secao', nargs='*')

    def handle(self, *args, **options):

        if len(options['cod_secao']) == 0:
            materiais = Material.objects.all()
        else:
            cod_secoes = options['cod_secao']
            materiais = Material.objects.filter(
                Q(familia_selecionada=True, familia__secao__cod_secao__in=cod_secoes) |
                Q(familia_selecionada=False, secao__isnull=True, secoes_possiveis__cod_secao__in=cod_secoes) | 
                Q(secao__cod_secao__in=cod_secoes)).distinct()

        print(u"%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            u"Setor",
            u"Cod. Seção",
            u"Seção",
            u"Cod. Grupo",
            u"Grupo",
            u"Cod. Subgrupo",
            u"Subgrupo",
            u"Cod. Familia",
            u"Familia",
            u"Cod. Material",
            u"Material",
            ))
        for m in materiais:
            if m.familia is not None:
                setor = m.familia.secao.setor.setor
                secao = m.familia.secao.secao
                cod_secao = m.familia.secao.cod_secao
                cod_grupo = m.familia.cod_grupo
                grupo = m.familia.grupo
                cod_subgrupo = m.familia.cod_subgrupo
                subgrupo = m.familia.subgrupo
                cod_familia = m.familia.cod_familia
                familia = m.familia.familia
            elif m.secao is not None:
                setor = m.secao.setor.setor
                secao = m.secao.secao
                cod_secao = m.secao.cod_secao
                cod_grupo = ''
                grupo = ''
                cod_subgrupo = ''
                subgrupo = ''
                cod_familia = ''
                familia = ''
            else:
                setor = ', '.join([ u'%s' % x.setor.setor for x in m.secoes_possiveis.all() ])
                secao = ', '.join([ u'%s' % x.secao for x in m.secoes_possiveis.all() ])
                cod_secao = ', '.join([ u'%s' % x.cod_secao for x in m.secoes_possiveis.all() ])
                cod_grupo = ''
                grupo = ''
                cod_subgrupo = ''
                subgrupo = ''
                cod_familia = ''
                familia = ''

            print(u"%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
                setor,
                cod_secao,
                secao,
                cod_grupo,
                grupo,
                cod_subgrupo,
                subgrupo,
                cod_familia,
                familia,
                m.cod_material,
                m.material
                ))


