'''
Lee el fichero de microdatos del censo y extrae los campos
'''

import sys
import struct
from collections import namedtuple

FIELDS = '2s3s10s4s14s2s4s3s1s3s3s2s3s4s4s4s4s3s2s3s1s3s2s3s1s3s2s3s1s1s3s2s3s3s1s1s1s2s1s1s1s1s1s1s2s1s1s2s2s1s5s2s2s2s1s3s2s3s5s1s1s1s1s1s1s1s1s1s1s3s2s2s1s1s2s1s1s1s1s1s1s1s1s1s1s2s2s2s2s1s2s2s1s1s2s2s2s2s2s2s2s2s2s2s2s2s2s2s2s2s2s2s1s2s3s1s1s1s1s1s2s3s1s1s1s1s1s2s1s1s1s1s1s1s1s2s2s2s2s2s2s2s'

CENSUS_FIELDS = '''CPRO
CMUN
IDHUECO
NORDEN
FACTOR
MNAC
ANAC
EDAD
SEXO
NACI
CPAISN
CPRON
CMUNN
ANORES
ANOM
ANOC
ANOE
CLPAIS
CLPRO
CLMUNP
RES_ANTERIOR
CPAISUNANO
CPROUNANO
CMUNANO
RES_UNANO
CPAISDANO
CPRODANO
CMUNDANO
RES_DANO
SEG_VIV
SEG_PAIS
SEG_PROV
SEG_MUN
SEG_NOCHES
SEG_DISP
ECIVIL
ESCOLAR
ESREAL
TESTUD
TAREA1
TAREA2
TAREA3
TAREA4
HIJOS
NHIJOS
RELA
JORNADA
CNO
CNAE
SITU
CSE
ESCUR1
ESCUR2
ESCUR3
LTRABA
PAISTRABA
PROTRABA
MUNTRABA
CODTRABA
NVIAJE
MDESP1
MDESP2
TDESP
TENEN
CALE
ASEO
BADUCH
INTERNET
AGUACOR
SUT
NHAB
PLANTAS
PLANTAB
TIPOEDIF
ANOCONS
ESTADO
ASCENSOR
ACCESIB
GARAJE
PLAZAS
GAS
TELEF
ACAL
RESID
FAMILIA
PAD_NORDEN
MAD_NORDEN
CON_NORDEN
OPA_NORDEN
TIPOPER
NUCLEO
NMIEM
NFAM
NNUC
NGENER
ESTHOG
TIPOHOG
NOCU
NPARAIN
NPFAM
NPNUC
HM5
H0515
H1624
H2534
H3564
H6584
H85M
HESPHOG
MESPHOG
HEXTHOG
MEXTHOG
COMBINAC
EDADPAD
PAISNACPAD
NACIPAD
ECIVPAD
ESTUPAD
SITUPAD
SITPPAD
EDADMAD
PAISNACMAD
NACIMAD
ECIVMAD
ESTUMAD
SITUMAD
SITPMAD
EDADCON
NACCON
NACICON
ECIVCON
ESTUCON
SITUCON
SITPCON
TIPONUC
TAMNUC
NHIJO
NHIJOC
FAMNUM
TIPOPARECIV
TIPOPARSEX
DIFEDAD
'''

NAMES = namedtuple('CENSO', CENSUS_FIELDS)

def field_split(line):
    '''
    :param line (str): cadena con un registro del censo
    :return (namedtuple): tupla con la lista de campos
    '''
    line = line.strip()
    if len(line) < 280:
        line += ' ' * (280-len(line))
    return NAMES._make([s.decode('ascii')
                        for s in struct.unpack(FIELDS, line.encode('ascii'))])


#-----------------------------------------------------------------------------

def show(tp):
    for f in tp._fields:
        print('{:20}'.format(f), getattr(tp, f))


#-----------------------------------------------------------------------------

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        for line in f:
            data = field_split(line)
            print("\n-----------------------------")
            show(data)
