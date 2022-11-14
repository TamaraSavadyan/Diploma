from time import time
import numpy as np
from scipy.fftpack import fft
from matplotlib import pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askdirectory
from os import listdir, mkdir
from os.path import join, exists, isfile
from csv import reader, writer
from count_data_per_station import Seismology_automation
import re # regular stuff
 
class Seismology:
 
   '''
   READING ALL SIGNALS FROM ALL FILES IN A DIRECTORY
   '''
 
   def read_signals(self, path, new_folder_name):
 
       if not exists("%s/%s" % (path, new_folder_name)):
           mkdir("%s/%s" % (path, new_folder_name))
 
       all_signals_in_directory = dict()
 
       for filename in listdir(path):
           if filename.endswith(".txt"):
               with open(join(path, filename), 'r') as file:
 
                   time = list()
                   amplitude = list()
                   samples = list()
 
                   for i, row in enumerate(file):
                       if i == 0:
                           new_row = row.split(" ")
                           time_step = float(new_row[1])
 
                       else:
                           time.append(i*time_step)
                           amplitude.append(float(row))        
 
                       # saving data for every second (not time_step)   
                    #    elif not (i % (1/time_step)):
                    #        ampl = self.mean(samples)
                    #        amplitude.append(ampl)
                    #        samples.clear()
 
                    #        time.append(i*time_step)
 
                    #    else:
                    #        samples.append(float(row))     
 
 
               all_signals_in_directory.setdefault(filename, [time, amplitude])
 
       return all_signals_in_directory
 
 
   '''
   GETTING DISCRETISATION OF STATIONS (ladder function, cringe)
   '''
 
   def get_discretisation(self):
       seisma = Seismology_automation()
       stations = seisma.get_stations('./counted_stations.csv', 0)
       stations_dict = dict.fromkeys(stations, 0)
 
       while True:
           try:
               # shows dialog box and return the path
               path = askdirectory(title='Select Folder')
               files = [f for f in listdir(path) if isfile(join(path, f))]
 
               for file_name in files:
                   flag = 1
                   for i in range(len(file_name)):
                       if flag and file_name[i] == '.':
                           for j in range(i + 1, len(file_name)):
                               if flag and file_name[j] == '.':
                                   # print('i: ', i, 'j: ', j, 'here')
                                   for station in stations_dict.keys():
                                       # station = re.sub('\s+',' ',station).strip()
                                       # print(station, 'initial')
                                       # print(file_name[i + 1:j], station == file_name[i + 1:j])
                                       if station == file_name[i + 1:j] and not stations_dict[station]:
                                           # print(2, 'Im here')
                                           with open(join(path, file_name), 'r') as file:
                                               for i, row in enumerate(file):
                                                   if i == 0:
                                                       new_row = row.split(" ")
                                                       time_step = float(new_row[1])
                                                       break
 
                                               stations_dict[station] = 1/time_step
 
                                   flag = 0
                      
 
           except Exception as e:
               with open('stations_discretisation.csv', 'w') as file:
                   w = writer(file)
                   w.writerows(stations_dict.items())
                   # for key in stations_dict.keys():
                   #     file.write("%s\t%s\n" % (key, stations_dict[key]))
               return stations_dict
 
   '''
   CALCULATE FOURIER TRANSFORM
   '''
 
   def fourier_transform(self, signal, path, new_folder_name):
 
       if not exists("%s/%s" % (path, new_folder_name)):
           mkdir("%s/%s" % (path, new_folder_name))
 
       signal_fft = np.abs(fft(signal[1]))
       freq = list()
       for i in signal[0]:
           freq.append(1/i)
 
       return signal_fft, freq
 
   '''
   CALC MEAN FUNCTION
   '''
   def mean(self, samples):
       return sum(samples)/len(samples)   
 
   '''
   AVERAGE FUNCTION
   '''
 
   def average(self, amplitudes, window):
       # Initialize an empty list to store moving averages
       moving_averages = []
 
       # Loop through the array
       for i, ampl in enumerate(amplitudes):
           if i < len(amplitudes) - window + 1:
               # Calculate the average of current window
               window_average = np.sum(amplitudes[i:i + window]) / window
               # Store the average of current window in moving average list
               moving_averages.append(window_average)
 
           # appending last values of window size to avoid 'different sizes' error
           else:
               moving_averages.append(ampl)
      
 
       return moving_averages
 
   '''
   PLOTTING SIGNALS FUNCTION
   '''
   # plot.figure is out of function in order to increase productivity of a function
   # function is called 2*N times
   
 
   def plot_signal(self, x, y, filename, x_label='', y_label='', y_averaged=None, x_limit=[], path=None):
 
       plt.figure(figsize=(12, 8))

       plt.plot(x, y)
 
       # if was calculated average of amplitudes
       if y_averaged:
           plt.plot(x, y_averaged, label='average')
 
       # if limit of x axis was specicfied
       if x_limit:
           plt.xlim(x_limit[0], x_limit[1])
 
       plt.title(filename)
       plt.xlabel(x_label)
       plt.ylabel(y_label)
       plt.grid()
 
       # if path to store files was specified
       if path:
           normal_filename = filename[:-4]
           plt.savefig(join(path, normal_filename+".png"))
       else:
           plt.show()

       plt.close()    
 
 
def main():
   seism = Seismology()
 
   while True:
       try:
           path = askdirectory(title='Select Folder')
           signals_folder_name = 'signals'
           transformed_signals_folder_name = 'Fourier Transformed signals'
           signals = seism.read_signals(path, signals_folder_name)
 
           average_window = 5
 
           for filename, signal in signals.items():
               averaged_signal = seism.average(signal[1], average_window)
               ''' saving images '''
            #    seism.plot_signal(signal[0], signal[1], filename, "t, s", "Ampl", averaged_signal, path="%s/%s" % (path, signals_folder_name))
               ''' showing result '''
               seism.plot_signal(signal[0], signal[1], filename, "t, s", "Ampl", averaged_signal, x_limit=[20,80])
               ''' showing averaged only '''
            #    seism.plot_signal(signal[0], averaged_signal, filename, "t, s", "Ampl")
 
               signal_fft, freq = seism.fourier_transform(signal, path, transformed_signals_folder_name)
               averaged_fft = seism.average(signal_fft, average_window)
               ''' saving images '''
            #    seism.plot_signal(freq, signal_fft, filename, "freq, Hz", "FFT.abs", averaged_fft, x_limit=[0,1], path="%s/%s" % (path, transformed_signals_folder_name))
               ''' showing result '''
               seism.plot_signal(freq, signal_fft, filename, "freq, Hz", "FFT.abs", averaged_fft, x_limit=[0,1])
               ''' showing averaged only '''
            #    seism.plot_signal(freq, averaged_fft, filename, "freq, Hz", "FFT.abs", x_limit=[0, 0.1])
 
       except Exception as e:
           print(e)
           print("Canceled path picking")
           break
 
 
 
if __name__ == '__main__':
   main()
   # seism = Seismology()
   # stations_dict = seism.get_discretisation()
   # print(stations_dict)
