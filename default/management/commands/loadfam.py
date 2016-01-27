#encoding=utf8
from django.core.management.base import BaseCommand, CommandError
from default.models import Familia, Secao

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

                    cod_secao = register[COD_SECAO].zfill(2)
                    cod_grupo = register[COD_GRUPO].zfill(4)
                    cod_subgrupo = register[COD_SUBGRUPO].zfill(6)
                    cod_familia = register[COD_FAMILIA].zfill(9)

                    if cod_secao <>  cod_grupo[0:2]:
                        self.stdout.write(self.style.ERROR(str('ERRO: Código de seção não coincide: "%s".' % register).decode('ascii','ignore')))
                        continue
                    if cod_grupo <> cod_subgrupo[0:4]:
                        self.stdout.write(self.style.ERROR(str('ERRO: Código de grupo não coincide: "%s".' % register).decode('ascii','ignore')))
                        continue
                    if cod_subgrupo <> cod_familia[0:6]:
                        self.stdout.write(self.style.ERROR(str('ERRO: Código de sub grupo não coincide: "%s".' % register).decode('ascii','ignore')))
                        continue

                    familia, creado = Familia.objects.get_or_create(
                        secao = Secao.objects.get_or_create(
                            cod_secao=cod_secao,
                            secao=register[SECAO]
                            )[0],
                        cod_grupo=cod_grupo,
                        grupo=register[GRUPO],
                        cod_subgrupo=cod_subgrupo,
                        subgrupo=register[SUBGRUPO],
                        cod_familia=cod_familia,
                        familia=register[FAMILIA],
                        )

                    if creado:
                        self.stdout.write(self.style.SUCCESS(str(u'Familia "%s" criada com sucesso.' % str(familia).decode('ascii','ignore')).decode('ascii','ignore')))
                    else:
                        self.stdout.write(self.style.WARNING(str('Familia "%s" ja existe.' % familia).decode('ascii','ignore')))

