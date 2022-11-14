from matplotlib import pyplot as plt, cm
from matplotlib.widgets import CheckButtons
import numpy as np
from csv import reader

'''
GETTING DATA NEEDED TO PLOT
'''


def get_data(csv_file, pos, amount_of_rows_to_delete=2):
    data = []
    with open(csv_file, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if row[pos]:
                data.append(row[pos])

        for _ in range(amount_of_rows_to_delete):
            del data[0]

    return data


'''
GETTING UNIQUE OBSERVATION POINT NAME
'''


def getting_unique(csv_file, name_pos):
    names_set = set()

    with open(csv_file, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if row[name_pos].isupper():
                names_set.add(row[name_pos])

    return names_set


'''
PLOTTING
'''

def plot_stuff(x, y, names, data_label='not labeled', title='', unique_list=[],
               magnitude_list=[], date_list=[], earthquake_coord_list=[], earthquake_net_list=[]):

    plt.figure(figsize=(12, 8))
    # fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.2)

    # using matplotlib checkbuttons to show explicit data
    if unique_list:
        # print(unique_list)
        new_plots = []
        x_new = []
        y_new = []
        names_new = []

        for unique in unique_list:
            for i, record in enumerate(names):
                if unique == record[1]:
                    x_new.append(x[i])
                    y_new.append(y[i])
                    names_new.append(names[i])

            if x_new:
                # x_new.append(quake_coord)
                # y_new.append(quake_coord)
                date = 'some str'
                new_plot, = plt.plot(x_new, y_new, visible=False, linestyle=':',
                                     marker='h', markerfacecolor='purple', alpha=0.5, label=unique)
                # earthquake_plot, = plt.plot(x_new[0], y_new[0], marker='*', visible=False, label='earthquake')
                new_plots.append(new_plot)
                # new_plots.append(earthquake_plot)

                for i, record in enumerate(names_new):
                    plt.annotate(record[0], (x_new[i], y_new[i]), fontsize=8)
                    # plt.text(x_new[i], y_new[i], record[0], fontsize=8)

            plt.xlabel("latitude")
            plt.ylabel("longtitude")

            x_new.clear()
            y_new.clear()
            names_new.clear()

        # Make checkbuttons with all plotted lines with correct visibility
        # 4-tuple of floats rect = [left, bottom, width, height]
        rax = plt.axes([0.05, 0.6, 0.11, 0.25])
        labels = [str(line.get_label()) for line in new_plots]
        visibility = [line.get_visible() for line in new_plots]
        check = CheckButtons(rax, labels, visibility)

        def func(label):
            index = labels.index(label)
            new_plots[index].set_visible(not new_plots[index].get_visible())
            plt.draw()

        check.on_clicked(func)
    else:
        print('inside else')
        plt.plot(x, y, linestyle=':', marker='h',
                 markerfacecolor='purple', alpha=0.5, label=data_label)
        for i, record in enumerate(names):
            plt.annotate(record, (x[i], y[i]), fontsize=8)

    plt.title(title)
    # plt.legend(loc='upper right')
    plt.grid()
    plt.show()

'''
FUNCTIONS TO USE IN __main__ SECTION
'''


def count_observation_names():
    observation_names_pos = [0, 22, 43]
    observation_names = set()

    for i in observation_names_pos:

        unique_names = getting_unique('./initial-data/seismology_all.csv', i)
        observation_names.update(unique_names)

    return sorted(observation_names)


def main():

    station_names = get_data('./initial-data/seismology_all.csv', 3)
    net_names = get_data('./initial-data/seismology_all.csv', 0)
    lon = get_data('./initial-data/seismology_all.csv', 7)
    lat = get_data('./initial-data/seismology_all.csv', 6)
    dates = get_data('./initial-data/seismology_all.csv', 10)
    magnitudes = get_data('./initial-data/seismology_all.csv', 21)
    lon_earthquakes = get_data('./initial-data/seismology_all.csv', 17)
    lat_earthquakes = get_data('./initial-data/seismology_all.csv', 15)
    net_earthquakes = get_data('./initial-data/seismology_all.csv', 22)

    unique_observation_names = count_observation_names()
    # print(unique_observation_names)

    lon_y = list(map(float, lon))
    lat_x = list(map(float, lat))
    coord_earthquakes = list(zip(map(float, lat_earthquakes), map(float, lon_earthquakes)))

    all_names = list(zip(station_names, net_names))
    
    plot_stuff(lat_x, lon_y, all_names, unique_list=unique_observation_names)

if __name__ == '__main__':
    main()
    