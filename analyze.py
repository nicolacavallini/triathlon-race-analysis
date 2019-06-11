import xlrd
from datetime import datetime
from datetime import timedelta

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


def read_times_xls(filename,fraction):
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


if __name__ == "__main__":

    data_path = "./data/"
    data_files = ["2014-maschile-ledro.xls",
                  "2014-maschile-ledro.xls",
                  "2018-maschile-ledro.xls"]
    #
    times = np.zeros((0,))
    #
    for df in data_files:
        times = np.hstack((times,read_times_xls(data_path+df,"TEMPO_UFFICIALE")))

    data_files = ["2016-maschile-ledro.csv",
                  "2017-maschile-ledro.csv"]

    for df in data_files:
        times = np.hstack((times,read_ledro_csv_format(data_path+df)["total"]))

    fig, ax = plt.subplots(2,1)

    bins = np.arange(3480,7500,60)

    values = ax[0].hist(times,bins)

    plt.sca(ax[0])
    plt.xticks(bins, [])
    plt.grid(axis='x')
    plt.title('num of samples ='+str(times.shape[0]))


    res = ax[1].hist(times,bins, density=True,
                           cumulative=True)
    plt.sca(ax[1])

    xlabels = [str(timedelta(seconds=t)) for t in bins]


    plt.xticks(bins, xlabels, rotation=60)

    expected_percentile = [.7,.8]
    ylabels = [str(p) for p in expected_percentile]
    plt.yticks(expected_percentile, ylabels)

    plt.grid()

    plt.show()
