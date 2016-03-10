#encoding=utf8
from django.core.management.base import BaseCommand, CommandError
from default.models import *
from multiprocessing import Pool
from els.utils import ElasticFilesGenerator

class Command(BaseCommand):
    help = 'Realiza um save para cada material e paraleliza por seção.'

    def add_arguments(self, parser):
        pass
        parser.add_argument('cod_secao', nargs='*')

    def handle(self, *args, **options):

        if len(options['cod_secao']) == 0:
            materiais = Material.objects.all()
        else:
            materiais = Material.objects.filter(secoes_possiveis__cod_secao__in=options['cod_secao'])

        efg = ElasticFilesGenerator(ES_FAMILIAS_INDEX,ES_FAMILIAS_DOC_TYPE,ES_FAMILIAS_INDEX)

        for m in materiais:
            efg.add(m.index_dict(), m.index_key())

