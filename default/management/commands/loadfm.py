#encoding=utf8
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from default.models import *
from django.db.utils import IntegrityError

COD_SECAO = 0
SECAO = 1
COD_GRUPO = 2
GRUPO = 3
COD_SUBGRUPO = 4
SUBGRUPO = 5
COD_FAMILIA = 6
FAMILIA = 7
COD_MATERIAL = 8
MATERIAL = 9

            
class Command(BaseCommand):
    help = u'Carrega familias de materiais y materiais desde arquivo separado por tabuladores.'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+')
        parser.add_argument('--forcesec',
            action='store_true',
            dest='forcesec',
            default=False,
            help=u'Coloca a seção da familia indicada como a nova seção.')

    def handle(self, *args, **options):

        forcesec = options['forcesec']

        with open('loadfm.err', 'w') as ferr:

            for filepath in options['filepath']:
                with open(filepath, 'r') as f:
                    header = True
                    for line in f:

                        if header:
                            header = False
                            continue

                        register = line.strip('\r\n').split('\t')

                        if len(register) <> 10:
                            self.stdout.write(self.style.ERROR(u'ERRO: Registro com quantidade %d distinta de campos a esperada 10: "%s".' % (len(register), register)))
                            print(line,file=ferr)
                            continue

                        if register[COD_MATERIAL] == "":
                            self.stdout.write(self.style.ERROR(u'ERRO: Material não informado: "%s"' % register))
                            print(line,file=ferr)
                            continue

                        for i in range(len(register)):
                            register[i] = register[i].strip()


                        try:

                            try:

                                try:

                                    secao = Secao.objects.get(
                                        secao=register[SECAO]
                                        )

                                except Secao.DoesNotExist:
                                    
                                    secao = Secao.objects.create(
                                        cod_secao=register[COD_SECAO],
                                        secao=register[SECAO]
                                        )

                                    secao.refresh_from_db()

                            except IntegrityError:
                                secao = Secao.objects.get(cod_secao=register[COD_SECAO])
                                self.stdout.write(self.style.ERROR(u'ERRO: Seção %s já existe e difiere do registro fornecido: "%s".' % (secao, register)))
                                print(line.strip(),file=ferr)
                                continue


                            try:
                                
                                try:

                                    familia = Familia.objects.get(
                                        secao = secao,
                                        grupo=register[GRUPO],
                                        subgrupo=register[SUBGRUPO],
                                        familia=register[FAMILIA],
                                        )

                                except Familia.DoesNotExist:

                                    familia = Familia.objects.create(
                                        secao = secao,
                                        cod_grupo=register[COD_GRUPO],
                                        grupo=register[GRUPO],
                                        cod_subgrupo=register[COD_SUBGRUPO],
                                        subgrupo=register[SUBGRUPO],
                                        cod_familia=register[COD_FAMILIA],
                                        familia=register[FAMILIA],
                                        )

                                    familia.refresh_from_db()
                                    self.stdout.write(self.style.SUCCESS(u'Familia "%s" criada com sucesso.' % familia))

                            except IntegrityError:
                                familia = Familia.objects.get(cod_familia=register[COD_FAMILIA])
                                self.stdout.write(self.style.ERROR(u'ERRO: Familia %s já existe e difiere do registro fornecido: "%s".' % (familia, register)))
                                print(line.strip(),file=ferr)
                                continue


                            try:

                                try:

                                    material = Material.objects.get(
                                        cod_material=register[COD_MATERIAL],
                                        )

                                except Material.DoesNotExist:

                                    material = Material.objects.create(
                                        cod_material=register[COD_MATERIAL],
                                        material=register[MATERIAL],
                                        )

                                    material.refresh_from_db()

                                    self.stdout.write(self.style.SUCCESS(u'Material "%s" criado com sucesso.' % material))

                                material.secoes_possiveis.add(secao)

                                if forcesec:
                                    if material.secao is not None:
                                        material.secao = secao

                            except IntegrityError:
                                material = Material.objects.get(cod_material=register[COD_MATERIAL])
                                self.stdout.write(self.style.ERROR(u'ERRO: Material %s já existe na seção %s e difiere do registro fornecido: "%s".' % (material, material.secoes_possiveis.all(), register)))
                                print(line.strip(),file=ferr)
                                continue

                            if material.familia is not None:
                                if material.familia.id == familia.id:
                                    continue
                            material.familia = familia
                            material.save()

                        except CodigoSecaoNaoCoincide:
                            self.stdout.write(self.style.ERROR(u'ERRO: Código de seção não coincide: "%s".' % register))
                            print(line.strip(),file=ferr)
                        except CodigoGrupoNaoCoincide:
                            self.stdout.write(self.style.ERROR(u'ERRO: Código de grupo não coincide: "%s".' % register))
                            print(line.strip(),file=ferr)
                        except CodigoSubGrupoNaoCoincide:
                            self.stdout.write(self.style.ERROR(u'ERRO: Código de sub grupo não coincide: "%s".' % register))
                            print(line.strip(),file=ferr)
                        except SecoesNaoCoincidem:
                            self.stdout.write(self.style.ERROR(u'ERRO: Material %s tem seção distinta que a familia %s.' % (material,familia,) ))
                            print(line.strip(),file=ferr)
                        except UnicodeDecodeError:
                            self.stdout.write(self.style.ERROR(u'ERRO: Erro unicode no registro: %s' % register ))
                            print(line.strip(),file=ferr)
                            

