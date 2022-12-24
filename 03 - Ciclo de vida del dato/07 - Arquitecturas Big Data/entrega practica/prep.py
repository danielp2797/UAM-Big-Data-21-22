import pandas as pd
import yfinance as yf # doc -> https://pypi.org/project/yfinance/
from datetime import datetime
import numpy as np
from sklearn.preprocessing import StandardScaler

def compute_PSY(df, window=14):  # (pd.DataFrame, int)
	# calcula el índice financiero PSY. Implementación consultada en: https://www.investopedia.com/articles/trading/03/010603.asp
	
	for ind, value in enumerate(df.PressureBool):
		df.loc[ind, 'PSY'] = sum(df.PressureBool[ind-window:ind])/window
		
	return 0
	
def compute_RSI(df, window=14):  # (pd.DataFrame, int)
	# calcula el índice financiero RSI. Implementación consultada en: https://www.investopedia.com/terms/r/rsi.asp
	
	for ind, value in enumerate(df.PressureBool):
		window_data = df.iloc[ind-window:ind]
		loss = window_data[~window_data.PressureBool]['PriceVar'].mean()
		gain = window_data[window_data.PressureBool]['PriceVar'].mean()
		df.loc[ind, 'RSI'] = 100 - 100/(1+(gain/loss))
		
	return 0
	
def compute_volatility(df, window=14):  # (pd.DataFrame, int)
	# calcula la volatilidad del activo (std).
	
	for ind, value in enumerate(df.PressureBool):
		df.loc[ind, 'volatility'] = np.std(df.Close[ind-window:ind])
		
	return 0

def today_date():  # void
	# devuelve la fecha actual en el formato pedido por el paquete yfinance.
	
	today = datetime.today().strftime("%Y-%m-%d")
	return today

if __name__ == '__main__':	
	print('Downloading data from yahoo finance...')
	data = yf.download(tickers='BTC-USD', start='2015-01-01', end=today_date())
	print('Downloaded successfully!')
	data.reset_index(inplace=True)
	data.columns = [col.replace(' ', '') for col in data.columns] # se eliminan espacios en blanco de los nombres de columna
	
	print('Computing Financial indexes...')
	
	data['PressureBool'] = data.Close.shift(1) > data.Close
	data['PriceVar'] = (data.Close-data.Close.shift(1))/data.Close.shift(1) * 100
	data['VolumeVar'] = (data.Volume-data.Volume.shift(1))/data.Volume.shift(1) * 100

	compute_PSY(data)
	compute_RSI(data)
	compute_volatility(data)

	scaler = StandardScaler()
	data.iloc[:, 1:] = scaler.fit_transform(data.iloc[:, 1:])
	
	print('Financial indexes successfully computed!')

	data = data.dropna()

	data.to_json('data/elasticData/BTC-USD-analysis.json', date_format='iso')
	data.to_parquet('hdfs://localhost:9000/bitcoin/input/BTC-USD-analysis.parquet', partition_cols=['PressureBool'], index=False)


