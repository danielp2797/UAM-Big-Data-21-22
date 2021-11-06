import sys
import os
from pathlib import Path


class CSV:  # clase para leer ficheros de texto

    def __init__(self, csv_file):

        self.path = Path(csv_file).absolute()

        with open(self.path, 'r') as target_file:
            lines_content = [line.rstrip('\n') for line in target_file]

        target_file.close()

        self.content = [[value.strip() for value in line.split(',')] for line in lines_content]

        self.col_num = len(self.content[0])
        self.row_num = len(self.content)

    def dtypes(self):
        # only 3 data types are suported: float, str or int 
        # decimal punctuation is assumed to be unique: '.' ==> float

        flag = [False for _ in range(self.col_num)]
        types = ['str' for _ in range(self.col_num)]

        for line in self.content:

            if all(flag):
                return types  # list of strings

            else:

                for col_index, item in enumerate(line):

                    if (item == '?') or (flag[col_index]):
                        continue

                    try:  # step1: checks if the item is an integer

                        int(item)
                        types[col_index], flag[col_index] = 'int', True

                    except ValueError:  # step2: checks if the item is a float
                        try:
                            float(item)
                            types[col_index], flag[col_index] = 'float', True

                        except ValueError:  # if it is not a float or int, it is a str (by default)
                            continue
        return types


if __name__ == '__main__':

    filename = sys.argv[1]
    options = sys.argv[2]

    csv = CSV(filename)

    for option in options:

        if option == 'p':

            result = ['' for _ in range(csv.col_num)]

            for j, dtype in enumerate(csv.dtypes()):

                if dtype in ['float', 'int']:
                    valid_values = [float(line[j]) for line in csv.content if line[j] != '?']
                    mean = sum(valid_values) / len(valid_values)
                    result[j] = round(mean, 2)

                if dtype == 'str':

                    column_values = sorted([line[j] for line in csv.content])
                    unique_values = list({line[j] for line in csv.content})
                    counts = [0 for _ in unique_values]

                    for i, item in enumerate(unique_values):
                        orig_index = column_values.index(item)
                        rever_index = column_values[::-1].index(item)
                        counts[i] = csv.row_num - orig_index - rever_index

                        result[j] = unique_values[counts.index(max(counts))]

            print(result)
            continue

        elif option == 's':

            result = [0 for _ in range(csv.col_num)]

            for j, dtype in enumerate(csv.dtypes()):

                if dtype in ['float', 'int']:
                    valid_values = [float(line[j]) for line in csv.content if line[j] != '?']
                    mean = sum(valid_values) / len(valid_values)

                    std = sum([x ** 2 for x in valid_values]) / len(valid_values) - mean ** 2
                    result[j] = round(std, 2)

                if dtype == 'str':
                    unique_values_num = len({line[j] for line in csv.content})
                    result[j] = unique_values_num

            print(result)

            continue

        elif option == 'n':

            result = [0 for _ in range(csv.col_num)]

            for j in range(csv.col_num):
                column = [line[j] for line in csv.content]
                invalid_values = column.count('?')
                result[j] = csv.row_num - invalid_values

            print(result)
            continue

        elif option == 'm':

            result = ['' for _ in range(csv.col_num)]

            for j, dtype in enumerate(csv.dtypes()):

                if dtype == 'float':
                    result[j] = min([float(line[j]) for line in csv.content if line[j] != '?'])

                if dtype == 'int':
                    result[j] = min([int(line[j]) for line in csv.content if line[j] != '?'])

                if dtype == 'str':

                    column_values = sorted([line[j] for line in csv.content])
                    unique_values = list({line[j] for line in csv.content})
                    counts = [0 for _ in unique_values]

                    for i, item in enumerate(unique_values):
                        orig_index = column_values.index(item)
                        rever_index = column_values[::-1].index(item)
                        counts[i] = csv.row_num - orig_index - rever_index

                        result[j] = unique_values[counts.index(min(counts))]

            print(result)
            continue

        elif option == 'M':

            result = ['' for _ in range(csv.col_num)]

            for j, dtype in enumerate(csv.dtypes()):

                if dtype == 'float':
                    result[j] = max([float(line[j]) for line in csv.content if line[j] != '?'])

                if dtype == 'int':
                    result[j] = max([int(line[j]) for line in csv.content if line[j] != '?'])

                if dtype == 'str':

                    column_values = sorted([line[j] for line in csv.content])
                    unique_values = list({line[j] for line in csv.content})
                    counts = [0 for _ in unique_values]

                    for i, item in enumerate(unique_values):
                        orig_index = column_values.index(item)
                        rever_index = column_values[::-1].index(item)
                        counts[i] = csv.row_num - orig_index - rever_index

                        result[j] = unique_values[counts.index(max(counts))]

            print(result)

