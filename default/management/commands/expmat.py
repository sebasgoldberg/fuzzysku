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
            materiais = Material.objects.all()
        else:
            materiais = Material.objects.filter(secoes_possiveis__cod_secao__in=options['cod_secao'])


        print(u"%s\t%s" % (
            u"Cod. Material",
            u"Cod. Familia",
            ))

        for m in materiais:
            print(u"%s\t%s" % (
                m.cod_material,
                m.familia.cod_familia,
                ))


