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
    help = 'Atualiza familias de materiais desde arquivo separado por tabuladores.'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+')

    def handle(self, *args, **options):

        with open('updfam.err', 'a+') as ferr:

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
                            familia = Familia.objects.get(
                                secao = Secao.objects.get(
                                    cod_secao=register[COD_SECAO].zfill(2),
                                    secao=register[SECAO]
                                    ),
                                grupo=register[GRUPO],
                                subgrupo=register[SUBGRUPO],
                                familia=register[FAMILIA],
                                )

                            familia.cod_grupo=register[COD_GRUPO].zfill(4)
                            familia.cod_subgrupo=register[COD_SUBGRUPO].zfill(6)
                            familia.cod_familia=register[COD_FAMILIA].zfill(9)

                            familia.save()

                            familia.refresh_from_db()
                            self.stdout.write(self.style.SUCCESS(u'Familia "%s" atualizada com sucesso.' % familia))

                        except Secao.DoesNotExist:
                            self.stdout.write(self.style.ERROR(u'ERRO: Seção não existe: "%s".' % register))
                            print(line,file=ferr)
                        except Familia.DoesNotExist:
                            self.stdout.write(self.style.ERROR(u'ERRO: Familia não existe: "%s".' % register))
                            print(line,file=ferr)
                        except CodigoSecaoNaoCoincide:
                            self.stdout.write(self.style.ERROR(u'ERRO: Código de seção não coincide: "%s".' % register))
                            print(line,file=ferr)
                        except CodigoGrupoNaoCoincide:
                            self.stdout.write(self.style.ERROR(u'ERRO: Código de grupo não coincide: "%s".' % register))
                            print(line,file=ferr)
                        except CodigoSubGrupoNaoCoincide:
                            self.stdout.write(self.style.ERROR(u'ERRO: Código de sub grupo não coincide: "%s".' % register))
                            print(line,file=ferr)
                        except IntegrityError:
                            self.stdout.write(self.style.ERROR(u'ERRO: Error de integridad: "%s".' % register))
                            print(line,file=ferr)


