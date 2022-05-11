from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, count, col
from pyspark.ml.stat import Correlation
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
import pandas as pd
import time
from pyspark.sql.functions import lag, col
from pyspark.sql.window import Window


def correlation_matrix(df, corr_columns, method='pearson'): # (pandas.DataFRame, list, str)
	
	# Calcula la matriz de correlaciones usando una app de Spark. Devuelve un dataframe de pandas con las matriz de correlaciones.
    vector_col = "corr_features"
    assembler = VectorAssembler(inputCols=corr_columns, outputCol=vector_col)
    df_vector = assembler.transform(df).select(vector_col)
    matrix = Correlation.corr(df_vector, vector_col, method)

    result = matrix.collect()[0]["pearson({})".format(vector_col)].values
    return pd.DataFrame(result.reshape(-1, len(corr_columns)), columns=corr_columns, index=corr_columns)

if __name__ == "__main__":
	
	print('\nLaunching Spark application...\n')
	spark = SparkSession \
		.builder \
		.appName("Consulta hipotesis") \
		.getOrCreate()
	

	print(f'\nSpark UI location: {spark.sparkContext.uiWebUrl}\n') # muestra la url de la UI

	sc = spark.sparkContext
	sc.setLogLevel("OFF")

	data = spark.read.parquet('hdfs://localhost:9000/bitcoin/input/BTC-USD-analysis.parquet')
	
	corr_cols = ['PSY', 'RSI','PriceVar', 'Volume', 'VolumeVar', 'volatility']
	corr_matrix = correlation_matrix(data, corr_cols)
	print('\n Correlation matrix between indexes and stock prices...')
	print(corr_matrix)
	data.write.format("parquet").save("hdfs://localhost:9000/bitcoin/output/BTC-USD-correlations.parquet")
