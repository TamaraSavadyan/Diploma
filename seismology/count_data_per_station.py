from csv import reader, writer, DictWriter
from tkinter import Tk
from tkinter.filedialog import askdirectory
from os import listdir
from os.path import isfile, join
 
 
class Seismology_automation:
 
   def get_stations(self, csv_file, station_name_position):
       stations_list = []
       with open(csv_file, 'r') as file:
           csv_reader = reader(file)
           if isinstance(station_name_position, int):
               for row in csv_reader:
                   stations_list.append(row[station_name_position])
                  
           else:
               for row in csv_reader:
                   for item in station_name_position:
                       if not row[item]:
                           continue
                       elif ' ' in row[item]:
                           new_strings = row[item].split(' ')
                           for i in new_strings:
                               stations_list.append(i)
                       else:
                           stations_list.append(row[item])
                      
       return stations_list
 
 
   def count_data(self, stations):
       stations_dict = dict.fromkeys(stations, 0)
 
       while True:
           try:
               # shows dialog box and return the path
               path = askdirectory(title='Select Folder')
               files = [f for f in listdir(path) if isfile(join(path, f))]
               for file_name in files:
                   flag = 1
                   for i in range(len(file_name)):
                       # print(i, 'here')
                       if flag and file_name[i] == '.':
                           for j in range(i + 1, len(file_name)):
                               # print(j)
                               # print(i, 'WOW')
                               if flag and file_name[j] == '.':
                                   for station in stations_dict.keys():
                                       if station == file_name[i + 1:j]:
                                           stations_dict[station] += 1
                                           # print(station, stations_dict[station])     
                                   flag = 0
                              
           except Exception as e:
               print(e)
               with open('counted_stations.csv', 'w') as file:
                   w = writer(file)
                   w.writerows(stations_dict.items())
                   # for key in stations_dict.keys():
                   #     file.write("%s\t%s\n" % (key, stations_dict[key]))
               return stations_dict
 
 
   def sort_data(self, data: dict):
       new_data = dict(
           sorted(data.items(), key=lambda item: item[1], reverse=True))
       with open('sorted_stations.csv', 'w') as file:
           w = writer(file)
           w.writerows(new_data.items())
           # for key in new_data.keys():
           #     file.write("%s\t%s\n" % (key, new_data[key]))
       return new_data
 
 
def main():
   seismolog = Seismology_automation()
 
   stations = seismolog.get_stations(
       csv_file='./initial-data/seismology_all.csv', station_name_position=(1, 2))
   # print('\n', stations)
 
   stations_dict = seismolog.count_data(stations)
 
 
   seismolog.sort_data(stations_dict)
 
 
 
if __name__ == '__main__':
   main()
