from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, count, col
import time

if __name__ == "__main__":

	spark = SparkSession \
		.builder \
		.appName("Procesado del censo") \
		.getOrCreate()

	print(f'\nSpark UI locatiion: {spark.sparkContext.uiWebUrl}\n') # muestra la url de la UI

	sc = spark.sparkContext
	sc.setLogLevel("WARN")

	data = spark.read.parquet('censo2011s.parquet')
	prov = spark.read.option("header", True).csv('codes-prov.csv')

	data_filtered = data.filter(data.CPAISN.isin([110, 123])) # filtro por pais de nacimiento francia(110) y portugal(123)

	data_filtered.groupBy('CPRO')\
				.agg(count(lit(1)).alias('RECUENTO__c'))\
				.join(prov, on='CPRO', how='left')\
				.select('NOMBRE_PRO', 'RECUENTO__c')\
				.orderBy(col('RECUENTO__c').desc())\
				.withColumn('RECUENTO_TOTAL__c', lit(data_filtered.count()))\
				.show(10)
