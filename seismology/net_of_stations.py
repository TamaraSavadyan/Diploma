from matplotlib import pyplot as plt, cm
from matplotlib.widgets import CheckButtons
import numpy as np
from csv import reader
 
'''
GETTING DATA NEEDED TO PLOT
'''
#!! Rewrite this function with *args or **kwargs (probably *args)
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
def plot_stuff(x, y, z, names, data_label='not labeled', title=''):

    plt.figure(figsize=(12, 8))

    # plt.scatter(x, y, z, c=z, cmap='seismic', alpha=0.1, label=data_label)
    # plt.colorbar()
    
    plt.plot(x, y, linestyle=':', marker='h', markerfacecolor='purple', alpha=0.5, label=data_label)
    # plt.fill_between(x, y)

    for i, record in enumerate(names):
        plt.annotate(record, (x[i], y[i]), fontsize=8)


    plt.title(title)
    plt.xlabel("latitude")
    plt.ylabel("longtitude")
    plt.legend(loc='upper right')
    plt.grid()
    plt.show()
 
'''
FUNCTIONS TO USE IN __main__ SECTION
'''
 
def count_observation_names():
   observation_names_pos = [0, 21, 42]
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
    alt = get_data('./initial-data/seismology_all.csv', 8)

    unique_observation_names = count_observation_names()
    # net_names_sorted = sorted(net_names)
    # station_names_sorted = [x for _, x in sorted(zip(net_names_sorted, station_names))]

    lon_y = list(map(float, lon))         
    lat_x = list(map(float, lat))
    alt_z = list(map(float, alt))

    all_names = zip(station_names, net_names)

    plot_stuff(lat_x, lon_y, alt_z, all_names)
 
 
 
if __name__ == '__main__':
    main()
