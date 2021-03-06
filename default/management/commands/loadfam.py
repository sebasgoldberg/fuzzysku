#encoding=utf8
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from default.models import *
from utils import ascii

COD_SECAO = 0
SECAO = 1
COD_GRUPO = 2
GRUPO = 3
COD_SUBGRUPO = 4
SUBGRUPO = 5
COD_FAMILIA = 6
FAMILIA = 7
            
class Command(BaseCommand):
    help = 'Carrega familias de materiais desde arquivo separado por tabuladores.'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+')

    def handle(self, *args, **options):

        with open('loadfam.err', 'a+') as ferr:

            for filepath in options['filepath']:
                with open(filepath, 'r') as f:
                    header = True
                    for line in f:
                        if header:
                            header = False
                            continue
                        line = line.strip('\r\n')
                        register = line.split('\t')
                        for i in range(len(register)):
                            register[i] = register[i].strip()

                        try:

                            try:

                                secao = Secao.objects.get(
                                    secao=register[SECAO]
                                    )

                            except Secao.DoesNotExist:

                                secao = Secao.objects.get_or_create(
                                    cod_secao=register[COD_SECAO].zfill(2),
                                    secao=register[SECAO]
                                    )[0]

                                secao.refresh_from_db()

                            cod_grupo=register[COD_GRUPO]
                            if cod_grupo <> '': 
                                cod_grupo.zfill(4)
                            cod_subgrupo=register[COD_SUBGRUPO]
                            if cod_subgrupo <> '': 
                                cod_subgrupo.zfill(6)
                            cod_familia=register[COD_FAMILIA]
                            if cod_familia <> '': 
                                cod_familia.zfill(9)


                            familia, creado = Familia.objects.get_or_create(
                                secao = secao,
                                cod_grupo=cod_grupo,
                                grupo=register[GRUPO],
                                cod_subgrupo=cod_subgrupo,
                                subgrupo=register[SUBGRUPO],
                                cod_familia=cod_familia,
                                familia=register[FAMILIA],
                                )

                            if creado:
                                familia.refresh_from_db()
                                self.stdout.write(self.style.SUCCESS(u'Familia "%s" criada com sucesso.' % familia))
                            else:
                                self.stdout.write(self.style.WARNING(ascii(u'Familia "%s" ja existe.' % familia)))


                        except CodigoSecaoNaoCoincide:
                            self.stdout.write(self.style.ERROR(ascii(u'ERRO: Código de seção não coincide: "%s".' % register)))
                            print(line,file=ferr)
                        except CodigoGrupoNaoCoincide:
                            self.stdout.write(self.style.ERROR(ascii(u'ERRO: Código de grupo não coincide: "%s".' % register)))
                            print(line,file=ferr)
                        except CodigoSubGrupoNaoCoincide:
                            self.stdout.write(self.style.ERROR(ascii(u'ERRO: Código de sub grupo não coincide: "%s".' % register)))
                            print(line,file=ferr)
                        except IntegrityError:
                            self.stdout.write(self.style.ERROR(ascii(u'ERRO: Error de integridad: "%s".' % register)))
                            print(line,file=ferr)

