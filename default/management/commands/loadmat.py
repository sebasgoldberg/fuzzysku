#encoding=utf8
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from default.models import Material, Secao
from django.db.utils import IntegrityError
from utils import ascii

COD_MATERIAL = 0
MATERIAL = 1
COD_SECAO = 2

class Command(BaseCommand):
    help = 'Carrega materiais desde arquivo separado por tabuladores.'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+')

    def handle(self, *args, **options):

        with open('loadmat.err', 'a+') as ferr:
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
                                )

                            material.secoes_possiveis.add(
                                Secao.objects.get(cod_secao=register[COD_SECAO])
                                )

                            if creado:
                                material.refresh_from_db()
                                self.stdout.write(self.style.SUCCESS(ascii(u'Material "%s" criado com sucesso.' % material)))
                            else:
                                self.stdout.write(self.style.WARNING(ascii(u'Material "%s" ja existe.' % material)))

                        except IntegrityError:

                            material = Material.objects.get(cod_material=register[COD_MATERIAL])
                            self.stdout.write(self.style.ERROR(ascii(u'ERRO: Material %s já existe na seção %s y difiere do registro fornecido: "%s".' % (material, material.secoes_possiveis.all(), register))))
                            print(line,file=ferr)

