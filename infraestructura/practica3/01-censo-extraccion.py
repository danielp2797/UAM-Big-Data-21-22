# -*- coding: utf-8 -*-
from __future__ import print_function

from pyspark.sql import SparkSession
spark = SparkSession \
    .builder \
    .appName("extraccion de datos del censo") \
    .getOrCreate()

sc = spark.sparkContext
sc.setLogLevel("WARN")

path = '/media/DiscoLocal/BigData/spark/'
path = 'file:///home/sparkuser/'

# Lee el fichero de microdatos
rdd = spark.sparkContext.textFile('censo2011s.txt.bz2')

# ¿cuántas particiones tenemos?
print("Partitions:", rdd.getNumPartitions())

import cparser
sc.addPyFile('cparser.py')
parsed = rdd.map( cparser.field_split )

from pyspark.sql import Row
# Definimos el objeto de fila usando los nombres de columna                       
CensoRow = Row( *cparser.NAMES._fields )
# Mapeamos cada fila a un objeto de fila                                          
rows = parsed.map( lambda x : CensoRow(*x) )

# RDD de Row a DataFrame                                                          
censo = spark.createDataFrame( rows )

print("Schema:")
censo.printSchema()

print("Size:", censo.count())

# Carga los nombres de municipio
sc.addFile('codes-cmun.csv')
cmun = spark.read.format('csv').option("header", True).load('codes-cmun.csv')

# Añade el nombre del municipio de residencia al Dataframe
cond = [censo.CMUN == cmun.CMUN, censo.CPRO == cmun.CPRO ]
censo_mun = censo.join(cmun, cond).drop(cmun.CPRO).drop(cmun.CMUN).drop(cmun.DC)

print("Schema + MUN:")
censo_mun.printSchema()

print( "Sample:" )
for row in censo_mun.limit(3).collect():
    print(row)

# Graba
censo_mun.write.format('parquet').mode('overwrite').save('censo2011s.parquet')
