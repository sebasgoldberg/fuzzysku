#encoding=utf8
from django.core.management.base import BaseCommand, CommandError
from default.models import Familia
from els.utils import ElasticFilesGenerator

COD_SECAO = 0
SECAO = 1
COD_GRUPO = 2
GRUPO = 3
COD_SUBGRUPO = 4
SUBGRUPO = 5
COD_FAMILIA = 6
FAMILIA = 7
            
class Command(BaseCommand):
    help = 'Carrega familias de materiais desde arquivo separado por tabuladores.'

    def handle(self, *args, **options):

        efg = ElasticFilesGenerator("skuhier","skuhier","skuhier")

        for familia in Familia.objects.all():

            efg.add({
                "cod_secao": familia.cod_secao,
                "secao": familia.secao,
                "cod_grupo": familia.cod_grupo,
                "grupo": familia.grupo,
                "cod_subgrupo": familia.cod_subgrupo,
                "subgrupo": familia.subgrupo,
                "cod_familia": familia.cod_familia,
                "familia": familia.familia,
                },
                familia.cod_familia)

            self.stdout.write(self.style.SUCCESS('Upload da familia "%s" feita com sucesso.' % str(familia).decode('ascii','ignore')))

