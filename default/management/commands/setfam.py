#encoding=utf8
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from default.models import *
from utils import ascii

COD_MATERIAL = 0
COD_FAMILIA = 1

class Command(BaseCommand):
    help = 'Asigna las familias a los materiales a partir de un archivo.'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+')

    def handle(self, *args, **options):

        with open('setfam.err', 'a+') as ferr:
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
                            m = Material.objects.get(
                                cod_material=register[COD_MATERIAL],
                                )
                            f = Familia.objects.get(
                                cod_familia=register[COD_FAMILIA],
                                )
                            m.familia = f
                            m.save()
                        except Material.DoesNotExist:
                            self.stdout.write(self.style.ERROR(ascii(u'Material %s não encontrado.' % register[COD_MATERIAL] )))
                            print(line,file=ferr)
                        except Familia.DoesNotExist:
                            self.stdout.write(self.style.ERROR(ascii(u'Familia %s não encontrada.' % register[COD_FAMILIA] )))
                            print(line,file=ferr)
                        except SecoesNaoCoincidem:
                            self.stdout.write(self.style.ERROR(ascii(u'Material %s tem seção distinta que a familia %s.' % (m,f,) )))
                            print(line,file=ferr)

