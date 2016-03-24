#encoding=utf8
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from default.models import *
from django.db.utils import IntegrityError

COD_MATERIAL = 0
COD_SECAO = 1

            
class Command(BaseCommand):
    help = u'Reclasifica materiais em novas seçoes.'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+')

    def handle(self, *args, **options):

        with open('novasec.err', 'w') as ferr:

            for filepath in options['filepath']:
                with open(filepath, 'r') as f:
                    header = True
                    for line in f:

                        if header:
                            header = False
                            continue

                        register = line.strip('\r\n').split('\t')

                        if len(register) <> 2:
                            self.stdout.write(self.style.ERROR(u'ERRO: Registro com quantidade %d distinta de campos a esperada 10: "%s".' % (len(register), register)))
                            print(line,file=ferr)
                            continue

                        for i in range(len(register)):
                            register[i] = register[i].strip()

                        try:
                            material = Material.objects.get(cod_material=register[COD_MATERIAL])
                        except Material.DoesNotExist:
                            self.stdout.write(self.style.WARNING(u'Material "%s" não existe.' % register[COD_MATERIAL]))
                            continue
                        
                        cod_secao = register[COD_SECAO].zfill(2)
                        try:
                            secao = Secao.objects.get(cod_secao=cod_secao)
                        except Secao.DoesNotExist:
                            self.stdout.write(self.style.ERROR(u'Seção "%s" não existe.' % cod_secao))
                            print(line,file=ferr)
                            continue
                        
                        if material.familia is not None:
                            if material.familia.secao <> secao:
                                self.stdout.write(self.style.ERROR(u'Seção %s da familia do material %s distinta da nova seção indicada %s.' % (
                                    material.familia.secao, material, secao)))
                                print(line,file=ferr)
                                continue

                        material.secao = secao
                        material.save()
                        material.refresh_from_db()
                        material.sugerir()
                        sugestoes = material.sugerir()
                        material.salvar_sugestoes(sugestoes)

                        self.stdout.write(self.style.SUCCESS(u'Nova seção %s aplicada ao material %s e sugestoes realizadas.' % (secao, material)))

