#encoding=utf8
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from default.models import *
from utils import ascii

COD_SECAO_SAP = 0
SECAO_SAP = 1

class Command(BaseCommand):
    help = 'Realiza o mapeamento entre as seções SAP e as novas seções.'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+')

    def handle(self, *args, **options):

        with open('mapsec.err', 'a+') as ferr:

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

                            secaoSAP = SecaoSAP.objects.get(cod_secao=register[COD_SECAO_SAP])

                            for desc_secao in register[2:]:
                                secao = Secao.objects.get(secao=desc_secao)
                                if SecaoSAP.objects.filter(pk=secaoSAP.pk, secoes_destino_possiveis=secao).exists():
                                    self.stdout.write(self.style.WARNING(u'Secao %s já existe como seção possivel da seção SAP %s.' % (secao, secaoSAP)))
                                else:
                                    secaoSAP.secoes_destino_possiveis.add(secao)
                                    self.stdout.write(self.style.SUCCESS(u'Secao %s adicionada como seção possivel à seção SAP %s.' % (secao, secaoSAP)))

                        except Secao.DoesNotExist:
                            self.stdout.write(self.style.ERROR(u'ERRO: Seção não existe: "%s".' % register))
                            print(line,file=ferr)

                        except SecaoSAP.DoesNotExist:
                            self.stdout.write(self.style.ERROR(u'ERRO: Seção SAP não existe "%s".' % register))
                            print(line,file=ferr)
