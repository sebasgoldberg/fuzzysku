#encoding=utf8
from django.core.management.base import BaseCommand, CommandError
from default.models import Material, Secao
from django.db.utils import IntegrityError

COD_MATERIAL = 0
MATERIAL = 1
COD_SECAO = 2

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

                    try:

                        material, creado = Material.objects.get_or_create(
                            cod_material=register[COD_MATERIAL],
                            material=register[MATERIAL],
                            secao=Secao.objects.get(cod_secao=register[COD_SECAO])
                            )
                    except IntegrityError:
                        material = Material.objects.get(cod_material=register[COD_MATERIAL])
                        self.stdout.write(self.style.ERROR(str('ERRO: Material %s já existe na seção %s y difiere do registro fornecido: "%s".' % (material, material.secao, register)).decode('ascii','ignore')))
                        continue

                    if creado:
                        self.stdout.write(self.style.SUCCESS('Material "%s" criado com sucesso.' % str(material).decode('ascii','ignore')))
                    else:
                        self.stdout.write(self.style.WARNING('Material "%s" ja existe.' % str(material).decode('ascii','ignore')))

