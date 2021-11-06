import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# cuando hay NaN en una columna, pandas siempre asume que es float u object, e ignora si la columna es entera.

if __name__ == '__main__':

    filename, options = sys.argv[1], sys.argv[2]
    path_to_file = Path(filename).absolute()
    data = pd.read_csv(path_to_file, header=None, na_values=['?'], low_memory=False)

    for option in options:

        if option == 'p':

            result = ['' for _ in range(data.shape[1])]

            for j, dtype in enumerate(data.dtypes.tolist()):  # calculo de medias

                if dtype in [np.float64, np.int64]:
                    result[j] = round(data.iloc[:, j].mean(), 2)

                else:  # calculo de la moda
                    result[j] = data.iloc[:, j].value_counts().index.tolist()[0]

            print(result)
            continue

        elif option == 's':

            result = [0 for _ in range(data.shape[1])]

            for j, dtype in enumerate(data.dtypes.tolist()):  # desviacion estandar
                if dtype in [np.float64, np.int64]:
                    result[j] = round(data.iloc[:, j].std(), 2)
                else:  # numero de valores distintos
                    result[j] = len(data.iloc[:, j].value_counts())

            print(result)
            continue

        elif option == 'n':

            result = data.shape[0] - np.array(data.isnull().sum().tolist())  # numero de valores no nulos
            print(result)
            continue

        elif option == 'm':

            result = ['' for _ in range(data.shape[1])]

            for j, dtype in enumerate(data.dtypes.tolist()):

                if dtype in [np.float64, np.int64]:  # calculo del minimo
                    result[j] = data.iloc[:, j].min()
                else:  # calculo del valor menos frecuente
                    result[j] = data.iloc[:, j].value_counts().index.tolist()[-1]
            print(result)
            continue

        elif option == 'M':

            result = ['' for _ in range(data.shape[1])]

            for j, dtype in enumerate(data.dtypes.tolist()):

                if dtype in [np.float64, np.int64]:  # calculo del maximo
                    result[j] = data.iloc[:, j].max()
                else:  # calculo del valor menos frecuente
                    result[j] = data.iloc[:, j].value_counts().index.tolist()[0]
            print(result)

        elif option == 'P':

            for j, dtype in enumerate(data.dtypes.tolist()):

                if dtype in [np.float64, np.int64]:

                    try: # salta si toda una columna es NaN
                        plt.hist(data.iloc[:, j], bins=int(data.shape[0]/20)+1)
                        plt.title(f'columna{j}')
                        plt.xlabel(f'variable{j}')
                        plt.ylabel(f'frecuencias')
                        plt.show()
                    except ValueError:
                        pass # se ignora la columna
                else:
                    data_aggregate = data.iloc[:, j].value_counts()
                    plt.pie(data_aggregate.values, labels=data_aggregate.index)
                    plt.title(f'columna{j}')
                    plt.show()


