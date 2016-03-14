#encoding=utf8
from django.core.management.base import BaseCommand, CommandError
from default.models import *
from multiprocessing import Pool
from els.utils import ElasticFilesGenerator
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

class Command(BaseCommand):
    help = 'Gera um arquivo de familias separado por tabuladores.'

    def add_arguments(self, parser):
        parser.add_argument('cod_secao', nargs='*')

    def handle(self, *args, **options):

        if len(options['cod_secao']) == 0:
            familias = Familia.objects.all()
        else:
            familias = Familia.objects.filter(secao__cod_secao__in=options['cod_secao'])

        print(u"%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            u"Setor",
            u"Cod. Seção",
            u"Seção",
            u"Cod. Grupo",
            u"Grupo",
            u"Cod. Subgrupo",
            u"Subgrupo",
            u"Cod. Familia",
            u"Familia",
            ))
        for f in familias:
            print(u"%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
                f.secao.setor.setor,
                f.secao.cod_secao,
                f.secao.secao,
                f.cod_grupo,
                f.grupo,
                f.cod_subgrupo,
                f.subgrupo,
                f.cod_familia,
                f.familia,
                ))

