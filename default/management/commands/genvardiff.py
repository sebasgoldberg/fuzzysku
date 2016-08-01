#encoding=utf8
from django.core.management.base import BaseCommand, CommandError
from default.models import *

import codecs
import sys
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

import re

class Command(BaseCommand):
    help = 'Realiza um save para cada material e paraleliza por seção.'

    def add_arguments(self, parser):
        parser.add_argument('cod_secao', nargs='*')

    def handle(self, *args, **options):

        print ('Setor\t'+
            'Cod. Generico ou variante\t'+
            'Generico ou variante\t'+
            'Cod. Familia G. ou V.\t'+
            'Familia G. ou V.\t'+
            'Cod. Variante\t'+
            'Variante\t'+
            'Cod. Familia V.\t'+
            'Familia V.\t')
        for m in Material.objects.all():
            if len(m.cod_material) >= 9 and re.search(r'00\d$',m.cod_material):
                grupo_genvar=Material.objects.filter(cod_material__startswith=m.cod_material[:-3]).exclude(cod_material=m.cod_material)
                for g in grupo_genvar:
                    if re.search(r'%s%s' % (m.cod_material[:-3], r'00\d$'),g.cod_material) or g.cod_material == m.cod_material[:-3]:
                        if g.familia <> m.familia:
                            setor = ''
                            cod_familia_g = ''
                            familia_g = ''
                            if g.familia is not None:
                                cod_familia_g = g.familia.cod_familia
                                familia_g = g.familia.familia
                                setor = g.familia.secao.setor.setor
                            cod_familia_v = ''
                            familia_v = ''
                            if m.familia is not None:
                                cod_familia_v = m.familia.cod_familia
                                familia_v = m.familia.familia
                                setor = m.familia.secao.setor.setor
                            print ('%(setor)s\t%(cod_generico)s\t%(generico)s\t%(cod_familia_g)s\t%(familia_g)s\t'+
                                '%(cod_variante)s\t%(variante)s\t%(cod_familia_v)s\t%(familia_v)s') % {
                                'setor': setor,
                                'cod_generico': g.cod_material,
                                'generico': g.material,
                                'cod_familia_g': cod_familia_g,
                                'familia_g': familia_g,
                                'cod_variante': m.cod_material,
                                'variante': m.material,
                                'cod_familia_v': cod_familia_v,
                                'familia_v': familia_v,
                                }

