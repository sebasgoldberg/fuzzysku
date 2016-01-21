#encoding=utf8
from django.core.management.base import BaseCommand, CommandError
from default.models import Sugestao

COD_MATERIAL = 0
COD_FAMILIA = 1

class Command(BaseCommand):
    help = 'Carrega materiais desde arquivo separado por tabuladores.'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+')

    def handle(self, *args, **options):

        for filepath in options['filepath']:
            with open(filepath, 'r') as f:
                header = True
                quan_sugeridos = 0
                quan_tot = 0
                for line in f:
                    if header:
                        header = False
                        continue
                    line = line.strip()
                    register = line.split('\t')
                    for i in range(len(register)):
                        register[i] = register[i].strip()

                    try:
                        Sugestao.objects.get(
                            material__cod_material=register[COD_MATERIAL],
                            familia__cod_familia=register[COD_FAMILIA],
                            )
                        quan_sugeridos = quan_sugeridos + 1
                    except Sugestao.DoesNotExist:
                        pass
                    
                    quan_tot = quan_tot + 1

        self.stdout.write(self.style.SUCCESS(str('Taixa de acierto %s%%.' % str(float(quan_sugeridos*100)/quan_tot) ).decode('ascii','ignore')))

