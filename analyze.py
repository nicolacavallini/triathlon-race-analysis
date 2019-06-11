import xlrd
from datetime import datetime

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

from os.path import isfile, join
from os import listdir

import csv

def get_files_list(data_path):
    return [f for f in listdir(data_path) if isfile(join(data_path, f))]

def string_to_time(input):
    time_list = []
    for ts in input:
        datetime_object = datetime.strptime(ts, '%H:%M:%S')
        time_list.append((datetime_object-datetime(1900,1,1)).total_seconds())

    return time_list


def read_times(filename,fraction):
    str_times_list = []
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheet_by_index(0)

    time_column_index = 0

    for j in range(1,sheet.ncols):
        if sheet.cell_value(0,j) == fraction:
            time_column_index = j


    for i in range(1,sheet.nrows):

        str = sheet.cell_value(i,time_column_index)

        if len(str)>0:

            str_times_list.append(str)

    return np.array(string_to_time(str_times_list));

def normalize_time(tl):
    min_t = np.amin(tl)
    max_t = np.amax(tl)
    return (tl-min_t)/(max_t-min_t)

def get_empty_results_dictionary():
    return {"total" : [], "swim" : [], "t1" : [], "bike" : [], "t2" : [], "run" : []}

def read_ledro_2017():

    time_strings = get_empty_results_dictionary()

    with open('./data/2017-maschile-ledro.csv', 'rb') as csvfile:

        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in csv_reader:
            #if i > 0:
            string = (','.join(','.join(item.split()) for item in row))
            line = string.replace(",,",",")
            line = line.replace(",,",",")

            time_strings["total"].append(line.split(",")[-15])
            time_strings["swim"].append(line.split(",")[-13])
            time_strings["t1"].append(line.split(",")[-10])
            time_strings["bike"].append(line.split(",")[-8])
            time_strings["t2"].append(line.split(",")[-5])
            time_strings["run"].append(line.split(",")[-3])



    times = {}

    for key, val in time_strings.items():
        time_strings[key] = val[1:]

    for key, val in time_strings.items():
        times[key] = string_to_time(val)
    return times


def read_ledro_csv_format(filename):

    time_strings = get_empty_results_dictionary()

    with open(filename, 'rb') as csvfile:

        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        csv_reader.next()

        for row in csv_reader:
            #if i > 0:
            string = (','.join(','.join(item.split()) for item in row))
            line = string.replace(",,",",")
            line = line.replace(",,",",")

            #print(line)
            # print(line.split(",")[-15])

            time_strings["total"].append(line.split(",")[-15])
            time_strings["swim"].append(line.split(",")[-13])
            time_strings["t1"].append(line.split(",")[-10])
            time_strings["bike"].append(line.split(",")[-8])
            time_strings["t2"].append(line.split(",")[-5])
            time_strings["run"].append(line.split(",")[-3])
            #print(time_strings["total"])
            # print(time_strings["swim"])
            # print(time_strings["t1"])
            # print(time_strings["bike"])
            # print(time_strings["t2"])
            # print(time_strings["run"])

    times = {}

    for key, val in time_strings.items():
        time_strings[key] = val[1:]

    for key, val in time_strings.items():
        times[key] = string_to_time(val)
    return times


if __name__ == "__main__":

    # print(ex)
    # print(new)


    times = read_ledro_csv_format('./data/2017-maschile-ledro.csv')
    #
    # print(times["total"])
    # print(times["t1"])
    # print(times["run"])

    # #times_list = read_times("2018.xls")
    #
    # data_path = "./data/"
    #
    # print(read_times(data_path+"2018-maschile-ledro.xls","TEMPO_UFFICIALE")[0:10])

    #print(normalize_time(read_times(data_path+"2019-maschile-milano.xls","TEMPO_UFFICIALE")))

    #
    # data_files = get_files_list(data_path)
    #
    # times = np.zeros((0,))
    #
    # for df in data_files:
    #     times = np.hstack((times,normalize_time(read_times(data_path+df,"TEMPO_UFFICIALE"))))

    fig, ax = plt.subplots()

    ax.hist(times["total"],40)

    plt.show()
