#encoding=utf8
from django.core.management.base import BaseCommand, CommandError
from default.models import *

COD_MATERIAL = 0
COD_FAMILIA = 1

class Command(BaseCommand):
    help = 'Carrega materiais desde arquivo separado por tabuladores.'

    def add_arguments(self, parser):
        parser.add_argument('cod_secao', nargs='*')

    def handle(self, *args, **options):

        materiais = Material.objects.filter(familia_selecionada=True, familia_sugerida=True)
        if len(options['cod_secao']) > 0:
            materiais = materiais.filter(secoes_possiveis__cod_secao__in=options['cod_secao'])

        quan_sugeridos = 0
        quan_tot = 0

        for material in materiais:

            try:
                Sugestao.objects.get(
                    material=material,
                    familia=material.familia,
                    )
                quan_sugeridos = quan_sugeridos + 1
            except Sugestao.DoesNotExist:
                pass
            
            quan_tot = quan_tot + 1
        
        if quan_tot == 0:
            taixa = 0
        else:
            taixa = float(quan_sugeridos*100)/quan_tot

        self.stdout.write(self.style.SUCCESS(u'Taixa de acierto %f%%.' % taixa ))

