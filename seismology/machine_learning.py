# use several model, check accuracy and etc.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from csv import reader, writer


def get_data(csv_file, pos, amount_of_rows_to_delete=1):
    data = []
    with open(csv_file, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if row[pos]:
                data.append(row[pos])

        for _ in range(amount_of_rows_to_delete):
            del data[0]
        

    return data


def marking_data(file_csv):

    soils = get_data(file_csv, 11)
    unique_soil = get_data(file_csv, 13)
    # classes = get_data(file_csv, 14)

    classes_dict = dict()
    for value, key in enumerate(unique_soil):
        classes_dict[key] = value

    result = []

    for soil in soils:
        for key, value in classes_dict.items():
            if soil == key:
                result.append(value)
            if soil not in classes_dict.keys():
                result.append(' ')

    return result

    # print(unique_soil)
    for key, value in classes_dict.items():
        print(f"{key} -> {value}")


res = marking_data('./seismology _data_for_learning.csv')

with open('result.txt', 'w') as file:
    for i in res:
        file.write(f'{i}\n')


        
