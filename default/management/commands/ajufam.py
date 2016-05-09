#encoding=utf8
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from default.models import *

SECAO = 0
GRUPO = 1
SUBGRUPO = 2
FAMILIA = 3
FAMILIA_DESTINO = 4
ELIMINAR = 5
            
class Command(BaseCommand):
    help = 'Carrega familias de materiais desde arquivo separado por tabuladores.'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+')

    def handle(self, *args, **options):

        with open('ajufam.err', 'a+') as ferr:

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


                            secao = Secao.objects.get(
                                secao=register[SECAO]
                                )

                            familia = Familia.objects.get(
                                secao = secao,
                                grupo=register[GRUPO],
                                subgrupo=register[SUBGRUPO],
                                familia=register[FAMILIA],
                                )

                            if register[ELIMINAR] == 'X':
                                if familia.material_set.exists():
                                    self.stdout.write(self.style.ERROR(u'ERRO: Familia ainda contem materiais, não pode ser eliminada: "%s".' % register))
                                    print(line.strip(),file=ferr)
                                else:
                                    familia.delete()
                                continue

                            try:

                                familia_destino = Familia.objects.get(
                                    secao = secao,
                                    grupo=register[GRUPO],
                                    subgrupo=register[SUBGRUPO],
                                    familia=register[FAMILIA_DESTINO],
                                    )

                                for m in familia.material_set.all():
                                    m.familia = familia_destino
                                    m.save()

                                familia.delete()

                            except Familia.DoesNotExist:
                                
                                familia.familia = register[FAMILIA_DESTINO].upper()
                                familia.save()

                                for m in familia.material_set.all():
                                    m.save()

                        except Secao.DoesNotExist:
                            self.stdout.write(self.style.ERROR(u'ERRO: A seção indicada não existe: "%s".' % register))
                            print(line.strip(),file=ferr)
                        except Familia.DoesNotExist:
                            self.stdout.write(self.style.ERROR(u'ERRO: A familia indicada não existe: "%s".' % register))
                            print(line.strip(),file=ferr)

                            if register[FAMILIA_DESTINO] <> '':

                                try:
                                    familia_destino = Familia.objects.get(
                                        secao = secao,
                                        grupo=register[GRUPO],
                                        subgrupo=register[SUBGRUPO],
                                        familia=register[FAMILIA_DESTINO],
                                        )
                                except Familia.DoesNotExist:
                                    continue

                                for m in familia_destino.material_set.all():
                                    m.familia = familia_destino
                                    try:
                                        m.save()
                                    except:
                                        print(m.cod_material)

                        except IntegrityError:
                            self.stdout.write(self.style.ERROR(u'ERRO: Error de integridad: "%s".' % register))
                            print(line.strip(),file=ferr)
                        except UnicodeDecodeError:
                            self.stdout.write(self.style.ERROR(u'ERRO: Unicode Error: "%s".' % register))
                            print(line.strip(),file=ferr)

