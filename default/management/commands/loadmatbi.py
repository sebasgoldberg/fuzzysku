#encoding=utf8
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from default.models import *
from django.db.utils import IntegrityError
from utils import ascii

COD_SECAO = 0
SECAO = 1
COD_MATERIAL = 2
MATERIAL = 3

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
                        for i in range(len(register)):
                            register[i] = register[i].strip().strip('"')


                        try:
                            
                            cod_secao = register[COD_SECAO].zfill(2)

                            secao_SAP, creado = SecaoSAP.objects.get_or_create(
                                cod_secao=cod_secao,
                                secao=register[SECAO]
                                )

                            if creado:
                                secao_SAP.refresh_from_db()

                        except IntegrityError:
                            secao_SAP = SecaoSAP.objects.get(cod_secao=register[COD_SECAO])
                            self.stdout.write(self.style.ERROR(ascii(u'ERRO: Seção SAP %s já existe e difiere do registro fornecido: "%s".' % (secao_SAP, register))))
                            print(line,file=ferr)
                            continue


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
                                self.stdout.write(self.style.SUCCESS(ascii(u'Material "%s" criado com sucesso.' % material)))
                            else:
                                self.stdout.write(self.style.WARNING(ascii(u'Material "%s" ja existe.' % material)))

                        except IntegrityError:

                            material = Material.objects.get(cod_material=register[COD_MATERIAL])
                            self.stdout.write(self.style.ERROR(ascii(u'ERRO: Material %s já existe na seção %s y difiere do registro fornecido: "%s".' % (material, material.secoes_possiveis.all(), register))))
                            print(line,file=ferr)

