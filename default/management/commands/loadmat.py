#encoding=utf8
from django.core.management.base import BaseCommand, CommandError
from default.models import Material

COD_MATERIAL = 0
MATERIAL = 1

class Command(BaseCommand):
    help = 'Carrega materiais desde arquivo separado por tabuladores.'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+')

    def handle(self, *args, **options):

        for filepath in options['filepath']:
            with open(filepath, 'r') as f:
                header = True
                for line in f:
                    if header:
                        header = False
                        continue
                    line = line.strip()
                    register = line.split('\t')
                    for i in range(len(register)):
                        register[i] = register[i].strip()
                    material, creado = Material.objects.get_or_create(
                        cod_material=register[COD_MATERIAL],
                        material=register[MATERIAL]
                        )

                    if creado:
                        self.stdout.write(self.style.SUCCESS('Material "%s" criado com sucesso.' % str(material).decode('ascii',ignore=True)))
                    else:
                        self.stdout.write(self.style.WARNING('Material "%s" ja existe.' % str(material).decode('ascii',ignore=True)))

