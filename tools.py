import xlrd
from datetime import datetime
from datetime import timedelta

import numpy as np

import matplotlib.pyplot as plt

from os.path import isfile, join
from os import listdir

import csv

def get_expected_pace():
    return {"swim" : 1*60+50., # sec/100m
             "t1" : 120., # sec
             "bike" : 27.5, # km/h
             "t2" : 120., #sec
             "run" : 5*60.+00.}#min/km

def get_distances():
    return {"swim" : 750., # m
             "t1" : 0., # sec
             "bike" : 20., # km
             "t2" : 120., #sec
             "run" : 5.}#km

def get_time_evaluation_formulas():
    return {"swim" : lambda d , p : d/100.* p,
            "t1" :     lambda d , p : p,
            "bike" :   lambda d , p : d/p*3600,
            "t2" :     lambda d , p : p,
            "run" :    lambda d , p : d*p }
            #given pace and distance avaluate time in seconds

def evaluate_times(paces,distances,formulas):
    n_times = {}
    n_times_string = {}
    time_total = 0.
    for k, v in paces.items():
        n_times[k] = formulas[k](distances[k],paces[k])
        print(k+": "+str(timedelta(seconds=int(n_times[k]))))
        time_total += n_times[k]

    n_times["total"] = time_total

    return n_times


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

    with open(filename, 'r') as csvfile:

        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        next(csv_reader)

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
