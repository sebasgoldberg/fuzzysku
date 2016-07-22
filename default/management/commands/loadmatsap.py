#encoding=utf8
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from default.models import *
from django.db.utils import IntegrityError

COD_MATERIAL = 0
COD_GRUPO_MERCADORIAS = 1
MATERIAL = 2

class Command(BaseCommand):
    help = 'Carrega materiais desde arquivo separado por tabuladores.'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+')

    def handle(self, *args, **options):

        with open('loadmatbi.err', 'a+') as ferr:
            for filepath in options['filepath']:
                with open(filepath, 'r') as f:
                    linenum = 0
                    for line in f:
                        linenum = linenum + 1
                        if linenum < 2:
                            continue
                        line = line.strip()
                        register = line.split('\t')
                        if len(register) <> 3:
                            continue
                        for i in range(len(register)):
                            register[i] = register[i].strip().strip('"')


                        try:
                            
                            cod_secao = register[COD_GRUPO_MERCADORIAS].zfill(9)[0:2]

                            secao_SAP = SecaoSAP.objects.get(
                                cod_secao=cod_secao,
                                )

                            try:

                                material, creado = Material.objects.get_or_create(
                                    cod_material=register[COD_MATERIAL],
                                    material=register[MATERIAL],
                                    secao_SAP = secao_SAP
                                    )

                                for secao in secao_SAP.secoes_destino_possiveis.all():
                                    material.secoes_possiveis.add(secao)

                                if creado:
                                    material.refresh_from_db()
                                    self.stdout.write(self.style.SUCCESS(u'Material "%s" criado com sucesso.' % material))
                                else:
                                    self.stdout.write(self.style.WARNING(u'Material "%s" ja existe.' % material))

                            except IntegrityError:

                                try:

                                    material = Material.objects.get(cod_material=register[COD_MATERIAL])
                                    material.secao_SAP = secao_SAP
                                    material.save()
                                    self.stdout.write(self.style.WARNING(u'Material "%s" ja existe.' % material))

                                except:

                                    self.stdout.write(self.style.ERROR(u'ERRO: Material %s já existe na seção %s y difiere do registro fornecido: "%s". Ao tentar atualizar a Seção SAP ocurriou um erro.' % (material, material.secoes_possiveis.all(), register)))
                                    print(line,file=ferr)

                        except SecaoSAP.DoesNotExist:
                            self.stdout.write(self.style.ERROR(u'ERRO: Seção SAP %s não existe. Registro fornecido: "%s".' % (cod_secao, register)))
                            print(line,file=ferr)
                            continue
                        except UnicodeDecodeError:
                            self.stdout.write(self.style.ERROR(u'ERROR: Erro de conversão unicode.' % register))
                            print(line,file=ferr)


