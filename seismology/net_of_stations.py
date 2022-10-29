from matplotlib import pyplot as plt, cm
from matplotlib.widgets import CheckButtons
import numpy as np
from csv import reader
 
'''
GETTING DATA NEEDED TO PLOT
'''
def get_data(csv_file, name_pos, net_names_pos, lat_pos, lon_pos, magnitude_pos=None):
    names, net_names, lat, lon, magnitudes = [], [], [], [], []
    with open(csv_file, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if row[name_pos]:
                names.append(row[name_pos])
                net_names.append(row[net_names_pos])
                lat.append(row[lat_pos])
                lon.append(row[lon_pos])
                if magnitude_pos:
                    magnitudes.append(row[magnitude_pos])

        for _ in range(2):
            del names[0]
            del net_names[0]
            del lat[0]
            del lon[0]
            # del magnitudes[0]
         
    return names, net_names, lon, lat
 
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
def plot_stuff(x, y, z, names):
 
   plt.figure(figsize=(12, 8))
 
   plt.scatter(x, y, z, c=z, cmap='seismic', alpha=0.5, label="Amount of records")
   plt.colorbar()
 
   for i, record in enumerate(names):
       plt.annotate(record, (x[i], y[i]), fontsize=8)
 
 
   plt.title("Amount of data at Caucasus stations")
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
 
   station_names, net_names, lon, lat = get_data('./initial-data/seismology_all.csv', 3, 0, 7, 6)
 
#    net_names_sorted = sorted(net_names)
#    station_names_sorted = [x for _, x in sorted(zip(net_names_sorted, station_names))]
 
   lon_x = list(map(float, lon))         
   lat_y = list(map(float, lat))

   z = np.linspace(1, 1, len(station_names)) 
   plot_stuff(lon_x, lat_y, z, (station_names, net_names))
 
 
 
if __name__ == '__main__':
   main()
 
#    count_observation_names()
