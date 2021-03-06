#encoding=utf8
from django.core.management.base import BaseCommand, CommandError
from default.models import *
from multiprocessing import Pool

COD_MATERIAL = 0
MATERIAL = 1

command = {}

def save_material(m):
    try:
        m.save()
    except:
        command['command'].stdout.write(command['command'].style.ERROR(u'Erro ao tentar salvar o material %s.' % m))

def save_material_secao_SAP(secao_SAP):
    for m in secao_SAP.material_set.all():
        save_material(m)
    command['command'].stdout.write(command['command'].style.SUCCESS(u'Seção SAP "%s": Materiales gravados.' % secao_SAP))


class Command(BaseCommand):
    help = 'Realiza um save para cada material e paraleliza por seção.'

    def add_arguments(self, parser):
        parser.add_argument('cod_secao', nargs='*')

    def handle(self, *args, **options):

        command['command'] = self

        secoes_especificas = False

        if len(options['cod_secao']) > 0:
            secoes = SecaoSAP.objects.filter(cod_secao__in=options['cod_secao'])
            secoes_especificas = True
        else:
            secoes = SecaoSAP.objects.all()


        pool = Pool(processes=32)
        pool.map(save_material_secao_SAP, [ s for s in secoes ] )

        if not secoes_especificas:
            for m in Material.objects.filter(secao_SAP__isnull=True):
                save_material(m)

