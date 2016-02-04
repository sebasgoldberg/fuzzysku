#encoding=utf8
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from default.models import *
from django.db.utils import IntegrityError

COD_SECAO = 0
SECAO = 1

class Command(BaseCommand):
    help = u'Carrega seções desde arquivo separado por tabuladores.'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+')

    def handle(self, *args, **options):

        with open('loadsec.err', 'a+') as ferr:

            for filepath in options['filepath']:
                with open(filepath, 'r') as f:
                    header = True
                    for line in f:
                        if header:
                            header = False
                            continue
                        line = line
                        line = line.strip()
                        register = line.split('\t')
                        if len(register) <> 2:
                            continue
                        for i in range(len(register)):
                            register[i] = register[i].strip()

                        try:
                            secao_desc = register[SECAO]
                            secao, creado = SecaoSAP.objects.get_or_create(
                                cod_secao=register[COD_SECAO],
                                secao=secao_desc
                                )

                            if creado:
                                self.stdout.write(self.style.SUCCESS(u'Seção SAP "%s" criada com sucesso.' % secao))
                            else:
                                self.stdout.write(self.style.WARNING(u'Seção SAP "%s" ja existe.' % secao))

                        except IntegrityError:
                            secao = SecaoSAP.objects.get(cod_secao=register[COD_SECAO].zfill(2))
                            self.stdout.write(self.style.ERROR(u'ERRO: Seção SAP %s já existe e difiere do registro fornecido: "%s".' % (secao, register)))
                            print(line,file=ferr)
