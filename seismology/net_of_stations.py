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
        # setting all lists and dicts needed to function
        new_plots = []
        x_unique = dict()
        y_unique = dict()
        names_unique = dict()

        # getting all coordinates for every net of observations
        for unique in unique_list:
                x_unique.setdefault(unique, [])
                y_unique.setdefault(unique, [])
                names_unique.setdefault(unique, [])
                for k, record in enumerate(names):
                    if unique == record[1]:
                        x_unique[unique].append(x[k])
                        y_unique[unique].append(y[k])
                        names_unique[unique].append(names[k])

            # looping through all net names to match it with observation names of stations
            # to show earthquake and stations that recorded it
        for i, net in enumerate(earthquake_net_list):
            if i == 10:
                break

            for unique in unique_list:
                if x_unique[unique]:
                    if net == unique:
                        x_unique[unique].append(earthquake_coord_list[i][0])
                        y_unique[unique].append(earthquake_coord_list[i][1])
                        label_name = date_list[i] + ' ' + unique
                        new_plot, = plt.plot(x_unique[unique], y_unique[unique], visible=False, linestyle=':',
                                                marker='h', markerfacecolor='red', alpha=0.5, label=label_name)
                        # earthquake_plot, = plt.plot(x_unique[0], y_unique[0], marker='*', visible=False, label='earthquake')
                        new_plots.append(new_plot)
                        # new_plots.append(earthquake_plot)
                        plt.annotate(magnitude_list[i], (x_unique[unique][-1], y_unique[unique][-1]), fontsize=10, color='red')
                        for j, name in enumerate(names_unique[unique]):
                            plt.annotate(name[0], (x_unique[unique][j], y_unique[unique][j]), fontsize=8)
                        
                        del x_unique[unique][-1]
                        del y_unique[unique][-1]

        plt.xlabel("latitude")
        plt.ylabel("longtitude")

        # Make checkbuttons with all plotted lines with correct visibility
        # 4-tuple of floats rect = [left, bottom, width, height]
        rax = plt.axes([0, 0.4, 0.155, 0.5])
        labels = [str(line.get_label()) for line in new_plots]
        visibility = [line.get_visible() for line in new_plots]
        check = CheckButtons(rax, labels, visibility)

        def func(label):
            index = labels.index(label)
            new_plots[index].set_visible(not new_plots[index].get_visible())
            plt.draw()

        check.on_clicked(func)

    
        plt.title(title)
        plt.grid()
        plt.show()    

    else:
        print('inside else')
        plt.plot(x, y, linestyle=':', marker='h',
                 markerfacecolor='purple', alpha=0.5, label=data_label)
        for i, record in enumerate(names):
            plt.annotate(record, (x[i], y[i]), fontsize=8)

        plt.title(title)
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

    for i in range(0, len(net_earthquakes[0:30]), 10):
        plot_stuff(lat_x, lon_y, all_names, unique_list=unique_observation_names,
        magnitude_list=magnitudes[i:i+10], date_list=dates[i:i+10], earthquake_coord_list=coord_earthquakes[i:i+10],
        earthquake_net_list=net_earthquakes[i:i+10])


if __name__ == '__main__':
    main()
    