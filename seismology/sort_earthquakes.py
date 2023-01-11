#!  I DON'T NEED THIS SHIT



from csv import reader, writer
from tkinter import Tk
from tkinter.filedialog import askdirectory
from os import listdir
from os.path import isfile, join


def get_stations(csv_file, station_name_position):
    stations_list = []
    simple_set = set()
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
                            simple_set = {i}  
                    else:
                        simple_set = {row[item]}
                
                if simple_set:
                    print(simple_set)
                    s = simple_set
                    print(s)
                    stations_list.append(s)
                    # print('my stations', stations_list)
                    # simple_set.clear()

    # for _ in range(2):
    #     del stations_list[0]

    return stations_list


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


def read_file_names():  # 20040502-090722_RU.AD2.00.SHZ.txt
    stations_dict = {}
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
                            for station in stations_dict.keys():
                                if station == file_name[i + 1:j]:
                                    stations_dict[station] += 1

                            flag = 0

    except Exception as e:
        print(e)
        with open('counted_stations.csv', 'w') as file:
            w = writer(file)
            w.writerows(stations_dict.items())
            # for key in stations_dict.keys():
            #     file.write("%s\t%s\n" % (key, stations_dict[key]))
        return stations_dict


def write_data(data: dict, filename):
    with open('%s.csv' % filename, 'w') as file:
        w = writer(file)
        w.writerows(data.items())

    return data


def main():

    # just station names
    station_names = get_stations(
        './initial-data/seismology_all.csv', (1, 2))
    lon = get_data('./initial-data/seismology_all.csv', 7)
    lat = get_data('./initial-data/seismology_all.csv', 6)
    alt = get_data('./initial-data/seismology_all.csv', 8)
    print(station_names)
    # for name in station_names:
    #     print(name)

    # earthquake data
    dates = get_data('./initial-data/seismology_all.csv', 10)
    magnitudes = get_data('./initial-data/seismology_all.csv', 21)
    depths = get_data('./initial-data/seismology_all.csv', 19)
    lon_earthquakes = get_data('./initial-data/seismology_all.csv', 17)
    lat_earthquakes = get_data('./initial-data/seismology_all.csv', 15)


if __name__ == '__main__':
    main()
