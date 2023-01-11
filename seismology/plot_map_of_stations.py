from matplotlib import pyplot as plt, cm
import numpy as np
from matplotlib.ticker import LinearLocator
from csv import reader
 
 
def get_data(csv_file, name_pos, amount_pos, lat_pos, lon_pos, alt_pos):
    names, amount, lat, lon, alt = [], [], [], [], []
    with open(csv_file, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if row[name_pos]:
                names.append(row[name_pos])
                amount.append(row[amount_pos])
                lat.append(row[lat_pos])
                lon.append(row[lon_pos])
                alt.append(row[alt_pos])

        for _ in range(2): 
            del names[0]
            del amount[0]
            del lat[0]
            del lon[0]
            del alt[0]
    
    return names, amount, lon, lat, alt
 
          
 
names, amount, lon, lat, alt = get_data('./initial-data/seismology_all.csv', 3, 4, 7, 6, 8)
# print(list(map(float, amount))) 
 
       
lat_x = list(map(float, lat))
lon_y = list(map(float, lon))
alt_z = list(map(int, alt))
amount_int = list(map(int, amount))
 
 
 
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
 
 
plot_stuff(lat_x, lon_y, amount_int, names)   
 
