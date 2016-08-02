#encoding=utf8
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from default.models import *
from django.db.utils import IntegrityError

COD_SECAO = 0
SECAO = 1
COD_MATERIAL = 2
MATERIAL = 3

criar_seacao = False

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
                        if linenum < 7:
                            header = False
                            continue
                        line = line.strip()
                        register = line.split(';')
                        if len(register) <> 5:
                            continue

                        for i in range(len(register)):
                            register[i] = register[i].strip().strip('"')

                        if register[MATERIAL] == 'Resultado':
                            continue
                        if register[MATERIAL] == 'Resultado global':
                            break

                        if criar_seacao:
                            try:
                                
                                cod_secao = register[COD_SECAO].zfill(2)

                                secao_SAP, creado = SecaoSAP.objects.get_or_create(
                                    cod_secao=cod_secao,
                                    secao=register[SECAO]
                                    )

                                if creado:
                                    secao_SAP.refresh_from_db()

                            except IntegrityError:
                                secao_SAP = SecaoSAP.objects.get(cod_secao=cod_secao)
                                self.stdout.write(self.style.ERROR(u'ERRO: Seção SAP %s já existe e difiere do registro fornecido: "%s".' % (secao_SAP, register)))
                                print(line,file=ferr)
                                continue
                        else:
                            cod_secao = register[COD_SECAO].zfill(2)
                            secao_SAP = SecaoSAP.objects.get(cod_secao=cod_secao)



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
                        except UnicodeDecodeError:
                            self.stdout.write(self.style.ERROR(u'ERROR: Erro de conversão unicode.' % register))
                            print(line,file=ferr)

