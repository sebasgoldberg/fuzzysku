#!/usr/bin/python
#encoding=utf8
__author__ = 'JSGold'

import datetime
import sys

#Cod Seção	Seção	Cod Grupo	Grupo	Cod SubGrupo	SubGrupo	Cod Familia	FAMILIA
COD_SECAO = 0
SECAO = 1
COD_GRUPO = 2
GRUPO = 3
COD_SUBGRUPO = 4
SUBGRUPO = 5
COD_FAMILIA = 6
FAMILIA = 7
            
from els.utils import ElasticFilesGenerator

class NoDataRecordException(Exception):
    pass

def parse(line):
    register = line.split('\t')
    if len(register) < 8:
        raise NoDataRecordException(u'Registro de datos no encontrado')
    for i in range(len(register)):
        register[i] = register[i].strip()
    return ({
        "cod_secao": int(register[COD_SECAO]),
        "secao": register[SECAO],
        "cod_grupo": int(register[COD_SUBGRUPO]),
        "grupo": register[GRUPO],
        "cod_subgrupo": int(register[COD_SUBGRUPO]),
        "subgrupo": register[SUBGRUPO],
        "cod_familia": int(register[COD_FAMILIA]),
        "familia": register[FAMILIA],
        })


def read(filename):

    lineNum = 0
    efg = ElasticFilesGenerator("skuhier","skuhier","skuhier")

    with open(filename, 'r') as f:
        for line in f:
            print line
            lineNum = lineNum + 1
            if lineNum <= 1:
                continue

            line = line.strip()
            #line = line.decode("utf8","replace")
            try:
                skuhier = parse(line)
                efg.add(skuhier,skuhier['cod_familia'])

            except NoDataRecordException:
                pass
            #except Exception:
                #print(line)

for f in sys.argv[1:]:
    read(f)
