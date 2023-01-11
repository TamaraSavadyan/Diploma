import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from csv import writer

def test1():

    t = np.arange(0.0, 2.0, 0.01)

    fig, ax = plt.subplots()
    lines = []
    for i in range(1, 5):
        s = np.sin(i*np.pi*t)
        l, = ax.plot(t, s, lw=2, label="%s Hz"%i)
        lines.append(l)

    plt.subplots_adjust(left=0.2)


    # Make checkbuttons with all plotted lines with correct visibility
    rax = plt.axes([0.05, 0.5, 0.1, 0.2])  # 4-tuple of floats rect = [left, bottom, width, height]
    labels = [str(line.get_label()) for line in lines]
    visibility = [line.get_visible() for line in lines]
    check = CheckButtons(rax, labels, visibility)


    def func(label):
        index = labels.index(label)
        lines[index].set_visible(not lines[index].get_visible())
        plt.draw()

    check.on_clicked(func)

    plt.show()


def test2():

    def change_separator(file_txt, new_file_name):
        with open(file_txt, 'r') as file:
            data = []
            for row in file:
                result = [x.replace('\t', ' ').strip() for x in row.split(' ') if x]
                var = ''.join(result)
                var.replace('\t', '')
                data.append(var)

        with open(new_file_name, 'w') as file:
            for row in data:
                file.write(f"{row}\n")

        return data
    
    result = change_separator('./test_file.txt', './new_names.txt')

    # print(result)

def test3():

    def find_unique(file_txt):
        with open(file_txt, 'r') as file:
            unique_set = set()
            for row in file:
                if row:
                    row.strip()
                    unique_set.add(row)
        return unique_set

    unique = find_unique('./uniq.txt')
    # print(unique)  
    for i in unique:
        print(i, end='')

test3()